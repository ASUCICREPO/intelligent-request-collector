import boto3

class EmailHandler:
    def __init__(self, uuid, email, from_email, region_name='us-east-1'):
        self.client = boto3.client('ses', region_name=region_name)
        self.email = email
        self.uuid = uuid
        self.from_email = from_email

    def send_email(self, body, subject= f'CIP Requirement Request'):
        response = self.client.send_email(
            Destination={
                'ToAddresses': [self.email]
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': """
                                    Explanation of Each Row

                                    Trait: This column specifies the characteristic or attribute being inquired about, such as "Usage," "Color," "Tuber shape," etc.

                                    Question_asked: This column contains the exact question posed to the user, aimed at understanding their preferences or conditions related to the trait.

                                    User_response: This shows a sample response that a user might give to the question. It indicates the user's preferences or specific requirements.

                                    Must_have_info: Indicates whether the information requested in this row is essential ("Yes") or just preferable ("Nice to have") for the evaluation process.

                                    Order_sequence_important: Specifies whether the question should be asked early in the sequence ("Yes - ask first") due to its importance in guiding the selection process.

                                    Valid_Answer: Provides guidelines on acceptable responses or constraints on the answers for this particular trait. For example, for the trait "Color," only specific colors like "Yellow, green, purple" are valid responses.
                                """ + f"\nThe Requirements for User {self.uuid} are :\n\n {body}",
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': f"{subject}: {self.uuid}",
                },
            },
            Source=self.from_email
        )
        return response