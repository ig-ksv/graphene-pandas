import pandas as pd
import graphene

from collections import OrderedDict

from graphene.types.objecttype import ObjectType, ObjectTypeOptions
from graphene.types.utils import yank_fields_from_attrs

from resolvers import get_attr_resolver, get_custom_resolver, get_default_id_resolver


def convert_field_type(column_type):
    if pd.api.types.is_object_dtype(column_type):
        field_type = graphene.List(graphene.String)
    elif pd.api.types.is_integer_dtype(column_type):
        field_type = graphene.List(graphene.Int)
    elif pd.api.types.is_float_dtype(column_type):
        field_type = graphene.List(graphene.Float)
    elif pd.api.types.is_bool_dtype(column_type):
        field_type = graphene.List(graphene.Boolean)
    elif pd.api.types.is_datetime64_any_dtype(column_type):
        field_type = graphene.List(graphene.DateTime)
    else:
        field_type = graphene.List(graphene.String)

    return field_type


def construct_fields(obj_type, model, exclude_fields=()):
    fields = OrderedDict()

    raw_fields = {column_name: column_type
                  for column_name, column_type
                  in model.dtypes.items()
                  if column_name not in exclude_fields}
    raw_fields["id"] = model.index.dtype

    for column_name, column_type in raw_fields.items():
        field_description = f"Here must be description of a field"
        field_resolver = get_custom_resolver(obj_type, column_name) or get_attr_resolver(model)
        if column_name == "id":
            field_resolver = get_default_id_resolver(model)
        field_type = convert_field_type(column_type)

        fields[column_name] = graphene.Field(resolver=field_resolver,
                                             type=field_type,
                                             description=field_description,
                                             required=None)
    return fields


class DataFrameObjectTypeOptions(ObjectTypeOptions):
    model = None
    id = None


class DataFrameObjectType(ObjectType):
    @classmethod
    def __init_subclass_with_meta__(
            cls,
            model=None,
            skip_registry=False,
            only_fields=(),
            exclude_fields=(),
            id=None,
            _meta=None,
            **options
    ):
        assert isinstance(model, pd.DataFrame), (
            "You need to pass a valid pandas DataFrame in " '{}.Meta, received "{}".'
        ).format(cls.__name__, model)

        if only_fields and exclude_fields:
            raise ValueError("The options 'only_fields' and 'exclude_fields' cannot be both set on the same type.")

        pd_fields = yank_fields_from_attrs(
            construct_fields(
                obj_type=cls,
                model=model,
                exclude_fields=exclude_fields,
            ),
            _as=graphene.Field,
            sort=False,
        )

        if not _meta:
            _meta = DataFrameObjectTypeOptions(cls)

        _meta.model = model

        if _meta.fields:
            _meta.fields.update(pd_fields)
        else:
            _meta.fields = pd_fields

        _meta.id = id or "id"

        super(DataFrameObjectType, cls).__init_subclass_with_meta__(
            _meta=_meta, **options
        )

    @classmethod
    def get_data(cls, info):
        model = cls._meta.model
        return [model.to_dict()]