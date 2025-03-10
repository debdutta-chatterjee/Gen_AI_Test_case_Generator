import requests
from requests.auth import HTTPBasicAuth
import json
import re
from src.state.state import UserStory

class AzureConnection:

    def get_user_story_details(self,url,pat,work_item):
        try:
            base_url = f'{url}/_apis/wit/workitems/{work_item}?api-version=6.0'
            session = requests.Session()
            session.auth = HTTPBasicAuth('', pat)
            response = session.get(base_url)

            if response.status_code == 200:
                details = response.json()
                
                description = details['fields'].get('System.Description', 'No description available'),
                acceptance_criteria = details['fields'].get('Microsoft.VSTS.Common.AcceptanceCriteria', 'No acceptance criteria available')
                title = details['fields']['System.Title']
                
                us = UserStory(
                acceptance_critera = self.remove_html_tags(str(acceptance_criteria)),
                business_context = self.remove_html_tags(str(description)),
                title = self.remove_html_tags(str(title))
                )
                return us
            else:
                raise ValueError(f"Failed to fetch user story details: {response.status_code} - {response.text}")
        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
        
    def remove_html_tags(self,text):
        """Remove HTML tags from a string."""
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', text)
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        text = text.replace('&nbsp;', ' ').replace('(', '').replace(')', '').strip()  # Remove &nbsp; and parentheses
        return re.sub(clean, '', text)
    
if __name__ == "__main__":
    organization_url = 'https://dev.azure.com/debduttachatterjee09/Agile-US'
    personal_access_token = 'GEQ76Z0xhwg7ewAkpl2pa7nrsnd74d4VQftOms7OkiwaORogU91WJQQJ99BCACAAAAAAAAAAAAASAZDO2sBr'
    project_name = 'Agile-US'
    work_item_id = '2'  

    ado = AzureConnection()
    details = ado.get_user_story_details(organization_url,personal_access_token,2)
    print(details)