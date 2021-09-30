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

class UpdateSupplier(graphene.Mutation):
    class Arguments:
       id = graphene.ID()
       name = graphene.String()
       notes = graphene.String()

    supplier = graphene.Field(SupplierType)

    @staticmethod
    def mutate(root, info, **kwargs):

        supplier_instance = Supplier.objects.get(pk=kwargs.get('id'))

        if supplier_instance:
            supplier_instance.name = kwargs.get('name')
            supplier_instance.notes = kwargs.get('notes')
            supplier_instance.save()

            return UpdateSupplier(supplier=supplier_instance)
        return UpdateSupplier(book=None)

class DeleteSupplier(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    supplier = graphene.Field(SupplierType)

    @staticmethod
    def mutate(root, info, id):
        supplier_instance = Supplier.objects.get(pk=id)
        supplier_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_supplier = CreateSupplier.Field()
    update_supplier = UpdateSupplier.Field()
    delete_supplier = DeleteSupplier.Field()

schema = graphene.Schema(query=Query)