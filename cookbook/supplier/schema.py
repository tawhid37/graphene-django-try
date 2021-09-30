import graphene
from graphene_django import DjangoObjectType
from .models import Supplier

class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier
        fields = ("id", "name", "notes")

class Query(graphene.ObjectType):
    all_suppliers = graphene.List(SupplierType)
    supplier = graphene.Field(SupplierType, supplier_id=graphene.Int())

    def resolve_all_suppliers(root, info):
        # We can easily optimize query count in the resolve method
        return Supplier.objects.all()
    
    def resolve_supplier(self, info, supplier_id):
        return Supplier.objects.get(pk=supplier_id)


class CreateSupplier(graphene.Mutation):
    supplier = graphene.Field(SupplierType)

    class Arguments:
        name = graphene.String()
        notes = graphene.String()

    def mutate(self, info, **kwargs):
        supplier = Supplier(name=kwargs.get('name'), notes=kwargs.get('notes'))
        supplier.save()
        return CreateSupplier(supplier=supplier)

class Mutation(graphene.ObjectType):
    create_supplier = CreateSupplier.Field()

schema = graphene.Schema(query=Query)