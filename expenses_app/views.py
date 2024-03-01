# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Expense, Balance, User
from .serializers import ExpenseSerializer
from .utils.email_utils import send_email_notification
from threading import Thread

class SplitExpenseAPIView(APIView):
    """
    API endpoint for splitting expenses among users.
    """

    def send_email_async(self, participants, total_amount, split_method):
        """
        Asynchronous method to send email notifications to participants.
        """
        send_email_notification(participants, total_amount, split_method)

    def post(self, request, format=None):
        """
        POST request to split expenses among users based on different methods.
        """
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            paid_by_user= serializer.validated_data['paid_by_user']
            paid_by_user_id=paid_by_user.id
            try:
                paid_by_user = User.objects.get(pk=paid_by_user_id)
            except User.DoesNotExist:
                return Response(f"User with ID {paid_by_user_id} does not exist", status=status.HTTP_400_BAD_REQUEST)

            total_amount = serializer.validated_data['total_amount']
            split_method = serializer.validated_data['split_method']
            participants_ids = serializer.validated_data['participants']


            if split_method == 'EQUAL':
                # Calculate split amount for each participant
                split_amount = total_amount / len(participants_ids)
                for participant in participants_ids:
                    if participant != paid_by_user:
                        balance, created = Balance.objects.get_or_create(user=participant, owes=paid_by_user, defaults={'amount': 0})
                        balance.amount += split_amount
                        balance.save()
                    # Start email sending thread    
                    email_thread = Thread(target=self.send_email_async, args=(participants_ids, split_amount, split_method))
                    email_thread.start()
            elif split_method == 'EXACT':
                breakpoint()
                exact_amounts = serializer.validated_data['exact_amounts']
                participants_ids = serializer.validated_data['participants']

                for participant_id, exact_amount in exact_amounts.items():
                    try:
                        participants = User.objects.get(pk=participant_id)
                    except User.DoesNotExist:
                        return Response(f"User with ID {participant_id} does not exist", status=status.HTTP_400_BAD_REQUEST)
                    if participants != paid_by_user:
                        balance, created = Balance.objects.get_or_create(user=participants, owes=paid_by_user,defaults={'amount': 0})
                        balance.amount += exact_amount
                        balance.save()
                        # Start email sending thread
                        email_thread = Thread(target=self.send_email_async, args=(participants_ids, exact_amount, split_method))
                        email_thread.start()


            elif split_method == 'PERCENT':
                percent_splits = serializer.validated_data['percent_splits']
                participants = serializer.validated_data['participants']
                total_percentage = sum(percent_splits.values())
                if total_percentage != 100:
                    return Response("Total percentage shares must be 100%", status=status.HTTP_400_BAD_REQUEST)

                for participant, percent_share in percent_splits.items():
                    split_amount = (total_amount * percent_share) / 100
                    if participant != paid_by_user:
                        balance, created = Balance.objects.get_or_create(user=participant, owes=paid_by_user)
                        balance.amount += split_amount
                        balance.save()
                    # Start email sending thread    
                    email_thread = Thread(target=self.send_email_async, args=(participants, split_amount, split_method))
                    email_thread.start()



            response_data = {
            "message": "Expense split successfully",
            "participants": [participant.name for participant in participants_ids],
            "total_amount": total_amount,
            "split_method": split_method
        }



            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
