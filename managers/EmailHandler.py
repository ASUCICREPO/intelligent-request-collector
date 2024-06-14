import boto3

class EmailHandler:
    def __init__(self, uuid, email, from_email, region_name='us-east-1'):
        self.client = boto3.client('ses', region_name=region_name)
        self.email = email
        self.uuid = uuid
        self.from_email = from_email

    def send_email(self, body, files, subject= f'CIP Requirement Request'):
        files_text = "The following are locations of the attached file/files:\n"
        for file in files:
            files_text += f"- {file}\n"
        response = self.client.send_email(
            Destination={
                'ToAddresses': [self.email]
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': files_text + """
                                    Information:

                                    Trait Tag: This column specifies the characteristic or attribute being inquired about, such as "Usage," "Color," "Tuber shape," etc.

                                    Collected Information: This column contains the exact question posed to the user, aimed at understanding their preferences or conditions related to the trait.
                                """ + f"\nThe gathered information is :\n\n {body}",
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