
from django.core.mail import send_mail

def send_email_notification(participants, total_amount, split_method):
    for participant in participants:
        subject = f'New Expense Added - Total Amount: {total_amount}'
        message = f'You have been added to a new expense. Total amount: {total_amount}, Split method: {split_method}'
        recipient_email = participant.email
        try:
            send_mail(subject, message, 'kapilgurjar912@gmail.com', [recipient_email], fail_silently=False)
        except Exception as e:
            # Handle any exceptions raised during email sending
            print(f"Failed to send email to {recipient_email}: {e}")
