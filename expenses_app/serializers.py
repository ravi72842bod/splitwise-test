from rest_framework import serializers
from . models import User

class ExpenseSerializer(serializers.Serializer):
    paid_by_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    split_method = serializers.ChoiceField(choices=['EQUAL', 'EXACT', 'PERCENT'])
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    exact_amounts = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False)
    percent_splits = serializers.DictField(child=serializers.IntegerField(), required=False)

    # def validate(self, data):
    #     split_method = data.get('split_method')
    #     if split_method == 'EXACT':
    #         exact_amounts = data.get('exact_amounts')
    #         if exact_amounts is None:
    #             raise serializers.ValidationError("Exact amounts are required for EXACT split method")
    #     return data
    def validate(self, data):
        split_method = data.get('split_method')
        percent_splits = data.get('percent_splits')
        exact_amounts = data.get('exact_amounts')

        if split_method == 'PERCENT' and not percent_splits:
            raise serializers.ValidationError("Percentage splits are required for 'PERCENT' split method")

        if split_method == 'EXACT' and not exact_amounts:
            raise serializers.ValidationError("Exact amounts are required for 'EXACT' split method")

        return data     
