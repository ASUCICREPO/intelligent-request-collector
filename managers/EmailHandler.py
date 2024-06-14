import boto3
import html 

class EmailHandler:
    def __init__(self, uuid, email, from_email, region_name='us-east-1'):
        self.client = boto3.client('ses', region_name=region_name)
        self.email = email
        self.uuid = uuid
        self.from_email = from_email

    def send_email(self, body, files, subject= f'CIP Requirement Request'):
        html_template = """
            <html>
                <body>
                    <strong>Requested By:</strong> {email} <br>
                    <strong>Attached File(s):</strong><br>
                    {file_list}
                    <strong>Information:</strong><br>
                    <table style="border-collapse: collapse; border: 1px solid black;">
                        <tr>
                            <th style="border: 1px solid black; padding: 5px;">Trait Tag</th>
                            <td style="border: 1px solid black; padding: 5px;">This column specifies the characteristic or attribute being inquired about, such as "Usage," "Color," "Tuber shape," etc.</td>
                        </tr>
                        <tr>
                            <th style="border: 1px solid black; padding: 5px;">Collected Information</th>
                            <td style="border: 1px solid black; padding: 5px;">This column contains the exact question posed to the user, aimed at understanding their preferences or conditions related to the trait.</td>
                        </tr>
                    </table><p>
                    <strong>Interview Results:</strong><br>
                    <pre><code>
                    {body}
                    </code></pre>
                </body>
            </html>
        """
        files_text = "<ul>"
        for file in files:
            files_text += f"<li>{file}</li>"
        files_text += "</ul>"

        values = {
            "email": self.email,
            "file_list": files_text,
            "body": html.escape(body)
        }

        final_html = html_template.format(**values)


        response = self.client.send_email(
            Destination={
                'ToAddresses': [self.email]
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': f"{final_html}",
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