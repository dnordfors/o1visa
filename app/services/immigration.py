# File: immigration.py
# Author: david nordfors

from openai import OpenAI
import json

resume = """<h2><br></h2><h2>Personal Information</h2><p><strong>Name:</strong> xxxxxx</p><p><strong>Nationality:</strong> Hungarian</p><p><strong>Current Residence:</strong> Budapest, Hungary</p><p><strong>Contact:</strong> xxxxx</p><h2>Professional Summary</h2><p>Accomplished economist with over 20 years of experience in economic research, policy formulation, and academic teaching. Recognized globally for contributions to macroeconomic theory and policy analysis. Proven track record in advising governmental and international organizations on economic strategies and reforms. Fluent in Hungarian, English, and German.</p><h2>Education</h2><ul><li><strong>Ph.D. in Economics</strong> - Corvinus University of Budapest, Hungary (2003)</li><li><strong>M.A. in Economics</strong> - University of Szeged, Hungary (1998)</li><li><strong>B.A. in Economics</strong> - University of Szeged, Hungary (1996)</li></ul><h2>Professional Experience</h2><ul><li><strong>Senior Economic Advisor</strong> - Hungarian Ministry of Finance, Budapest, Hungary (2015-Present)</li><li class="ql-indent-1">Advises on fiscal policy, economic reforms, and financial stability.</li><li class="ql-indent-1">Leads economic research projects and drafts policy recommendations.</li><li class="ql-indent-1">Represents Hungary in international economic forums.</li><li><strong>Professor of Economics</strong> - Corvinus University of Budapest, Hungary (2008-Present)</li><li class="ql-indent-1">Teaches courses in macroeconomics, international economics, and economic policy.</li><li class="ql-indent-1">Supervises doctoral research and theses.</li><li class="ql-indent-1">Publishes research papers in leading economic journals.</li><li><strong>Research Fellow</strong> - Institute of Economics, Hungarian Academy of Sciences, Budapest, Hungary (2003-2015)</li><li class="ql-indent-1">Conducted extensive research on macroeconomic stability and growth.</li><li class="ql-indent-1">Collaborated with international research institutions on joint projects.</li><li class="ql-indent-1">Presented findings at global economic conferences.</li></ul><h2>Publications</h2><ul><li>“Macroeconomic Stability in Emerging Markets” - Journal of Economic Perspectives (2020)</li><li>“Fiscal Policy and Economic Growth” - European Economic Review (2018)</li><li>“Globalization and Income Inequality” - World Development (2016)</li></ul><h2>Awards and Honors</h2><ul><li>Recipient of the Hungarian Academy of Sciences Award for Outstanding Research in Economics (2019)</li><li>Best Professor Award, Corvinus University of Budapest (2017)</li><li>Research Excellence Award, Institute of Economics, Hungarian Academy of Sciences (2014)</li></ul><h2>Languages</h2><ul><li>Hungarian (Native)</li><li>English (Fluent)</li><li>German (Fluent)</li></ul><h2>Professional Affiliations</h2><ul><li>Member, Hungarian Economic Association</li><li>Member, European Economic Association</li><li>Fellow, International Association for Applied Econometrics</li></ul><h2>References</h2><p>Available upon request</p><p>```</p>"""
openai_client = OpenAI()

class ImmigrationOfficer:
    def __init__(self, resume):

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "rate_likelihood_for_O1-A_visa",
                    "description": "Based on provided assessments, rate the overall likelihood that the applicant can qualify for an o1a visa by putting more work into the application.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rated likelihood": {
                                "type": "string",
                                "enum":["low","medium","high"],
                                "description": "Assessed overall likelihood that applicant can meet O1-A visa criteria",
                            },
                        },
                        "required": ["rated likelihood"],
                        "additionalProperties": False,
                    },
                },
                "strict": True,
            }
        ]

        self.assistant_instruction = '''# System Instruction
        You are an immigration officer evaluating applications for O1-A visas,
        To assess how a person is qualified for an O-1A immigration visa, you can refer to the [USCIS O-1 Visa page](https://www.uscis.gov/working-in-the-united-states/temporary-workers/o-1-visa-individuals-with-extraordinary-ability-or-achievement) for more information. There are eight criteria defined for O-1A qualification, which you can find in the [USCIS Policy Manual](https://www.uscis.gov/policy-manual/volume-2-part-m#) by clicking on the Appendices and expanding the section of 'Appendix: Satisfying the O-1A Evidentiary Requirements'.

        Your job is to predict if an applicant fulfills a select criterion of the eight criteria, the only information you have access to is the applicant's resume.
        '''
        self.resume_header = """<h1>Resume</h1><h1>provided by o1-a visa applicant, for evaluation.</h1>"""
        self.applicants_resume = self.resume_header + resume

        self.start_messages = [
            {
                'role': 'system',
                'content': self.assistant_instruction
            },
            {
                'role': 'user',
                'content': 'Here is the applicants resume: \n ' + self.applicants_resume
            },
        ]

        self.user_messages = [
            {
                'role': 'user',
                'content': '<p>How likely is it that the applicant is the kind of person who will fulfill the first criterion:</p><p><br></p><ol><li>Receipt of nationally or internationally recognized prizes or awards for excellence in the field of endeavor.</li><li class="ql-indent-1"><strong>What USCIS needs confirmed:</strong> The award should be recognized nationally or internationally as an achievement in the field. The award must be directly related to the applicant\'s field of expertise and be significant in nature. The applicant should provide documentation such as the name of the award, the criteria for receiving the award, the significance of the award in the field, and any press coverage or public recognition associated with the award.</li><li class="ql-indent-1"><strong>Examples:</strong> Nobel Prize, Pulitzer Prize, major industry-specific awards such as the ACM Turing Award for computing. Additional examples can include the Fields Medal in mathematics, the Grammy Awards in music, or the Academy Awards (Oscars) in film. The USCIS Policy Manual further specifies that lesser-known awards can also be considered if the applicant can demonstrate their significance and recognition within the field.</li></ol>'
            },
            {
                'role': 'user',
                'content': '<p>How likely is it that the applicant is the kind of person who will fulfill the second criterion:</p><p><br></p><ol><li>Membership in associations in the field which require outstanding achievements of their members, as judged by recognized national or international experts.</li><li class="ql-indent-1"><strong>What USCIS needs confirmed:</strong> Membership should be in associations that require members to demonstrate outstanding achievements in the field. The selection process for membership should be rigorous and based on significant contributions to the field.</li><li class="ql-indent-1"><strong>Examples:</strong> National Academy of Sciences, IEEE Fellows, American Medical Association.</li></ol><p><br></p>'
            },
            {
                'role': 'user',
                'content': '<p>How likely is it that the applicant is the kind of person who will fulfill the third criterion:</p><p><br></p><p>Published material in professional or major trade publications or major media about the individual and their work in the field.</p><ol><li class="ql-indent-1"><strong>What USCIS needs confirmed:</strong> The published material should be in a recognized professional or major trade publication. The content must focus on the individual\'s work and its impact on the field.</li><li class="ql-indent-1"><strong>Examples:</strong> Articles in \'Nature,\' \'Science,\' \'The Wall Street Journal,\' or industry-specific publications.</li></ol><p><br></p><p> Take into consideration: how likely is it that publications of the said kind will have written about the applicant, based on the typical profiles of the people that occur in their stories?</p>'
            },
            {
                'role': 'user',
                'content': '<p>How likely is it that the applicant is the kind of person who will fulfill the fourth criterion:</p><p><br></p><p>Participation on a panel, or individually, as a judge of the work of others in the same or an allied field.</p><ol><li class="ql-indent-1"><strong>What USCIS needs confirmed:</strong> The individual should have been invited to judge the work of others in their field, indicating a high level of expertise and recognition.</li><li class="ql-indent-1"><strong>Examples:</strong> Serving as a peer reviewer for scientific journals, judging at industry award ceremonies or competitions.</li></ol>'
            },
            {
                'role': 'user',
                'content': '<p>How likely is it that the applicant is the kind of person who will fulfill the fifth criterion:</p><p><br></p><p>Original scientific, scholarly, or business-related contributions of major significance in the field.</p><ol><li class="ql-indent-1"><strong>What USCIS needs confirmed:</strong> The contributions should be original and have had a significant impact on the field. These contributions should be recognized by peers and have led to advancements or new developments.</li><li class="ql-indent-1"><strong>Examples:</strong> Inventing a new technology, groundbreaking research findings, significant business innovations.</li></ol>'
            },
            {
                'role': 'user',
                'content': '<p>How likely is it that the applicant is the kind of person who will fulfill the sixth criterion:</p><p><br></p><p>Authorship of scholarly articles in professional journals or other major media in the field.</p><ol><li class="ql-indent-1"><strong>What USCIS needs confirmed:</strong> The individual should have authored scholarly articles that have been published in reputable journals or major media. These articles should contribute to the field and be recognized by peers.</li><li class="ql-indent-1"><strong>Examples:</strong> Publications in \'The New England Journal of Medicine,\' \'IEEE Transactions,\' \'Harvard Business Review.\'</li></ol>'
            },
            {
                'role': 'user',
                'content': '<p>How likely is it that the applicant is the kind of person who will fulfill the seventh criterion:</p><p><br></p><p>Employment in a critical or essential capacity for organizations and establishments that have a distinguished reputation.</p><ol><li class="ql-indent-1"><strong>What USCIS needs confirmed:</strong> The individual should have been employed in a role that is critical or essential to the success of a distinguished organization. The organization itself must be recognized for its excellence and contributions to the field.</li><li class="ql-indent-1"><strong>Examples:</strong> Senior roles at Google, NASA, Mayo Clinic.</li></ol><p><br></p>'
            },
            {
                'role': 'user',
                'content': '<p>How likely is it that the applicant is the kind of person who will fulfill the eighth criterion:</p><p><br></p><p>High salary or other significantly high remuneration for services, evidenced by contracts or other reliable evidence.</p><ol><li class="ql-indent-1"><strong>What USCIS needs confirmed:</strong> The individual should receive a high salary or significant remuneration that is indicative of their extraordinary ability. This should be evidenced by contracts or other reliable documentation.</li><li class="ql-indent-1"><strong>Examples:</strong> Employment contracts showing salaries in the top percentile for the field, significant consulting fees.</li></ol>'
            },
        ]

        self.prompt_report = {
            'role': 'user',
            'content': '<p>Write a report to the USCIS:</p><p><br></p><ul><li>Based on previous assessments, predict an overall likelihood that the applicant can qualify for an o1a visa by putting more work into the application. Explain how you came to that assessment.</li></ul>'
        }
        self.prompt_letter = {
            'role': 'user',
            'content': '<ul><li>draft a letter to the applicant, encouraging or discouraging further work with the application, giving the applicant a picture of further work required.</li></ul>'
        }

        self.prompt_rating = {
            'role': 'user',
            'content': 'rank the overall likelihood that the applicant can qualify for an o1a visa by putting more work into the application. '
        }

    def evaluate_applicant(self):
        settings = {'frequency_penalty': 0, 'max_tokens': 4000, 'model': 'gpt-4o', 'n': 1, 'presence_penalty': 0,
                    'temperature': 0.7, 'user': 'Ugsfg7mEh5'}
        respfmt = {}
        messages = self.start_messages
        responses = []

        # assess eligibility for criteria
        for crit in self.user_messages:
            print(crit)
            messages.append(crit)
            res = openai_client.chat.completions.create(messages=messages, **respfmt, **settings).dict()
            responses.append(res)
            assistant_msg = res['choices'][0]['message']
            messages.append(assistant_msg)
            print(assistant_msg)

        # write report
        messages.append(self.prompt_report)
        print(self.prompt_report)
        res = openai_client.chat.completions.create(messages=messages, **respfmt, **settings).dict()
        responses.append(res)
        assistant_msg = res['choices'][0]['message']
        messages.append(assistant_msg)
        self.assessment_report = assistant_msg
        print(assistant_msg)

        # write letter
        messages.append(self.prompt_letter)
        print(self.prompt_letter)
        res = openai_client.chat.completions.create(messages=messages, **respfmt, **settings).dict()
        responses.append(res)
        assistant_msg = res['choices'][0]['message']
        messages.append(assistant_msg)
        self.letter_to_candidate = assistant_msg
        self.messages = messages

        # rate likelihood
        msg = [
            {
                "role": "system",
                "content": "Use the supplied tools to assist the user."
            },
            {
                'role':'user',
                'content':'Based on provided assessments, rate the overall likelihood that the applicant can qualify for an o1a visa by putting more work into the application: \n '+json.dumps(messages)
            }
        ]
        res = openai_client.chat.completions.create(messages=msg,tools=self.tools, **respfmt, **settings).dict()
        responses.append(res)
        try:
            self.rated_likelihood = [d['function']['arguments'] for d in res['choices'][0]['message']['tool_calls'] if d['function']['name']=='rate_likelihood_for_O1-A_visa']
        except:
            self.rated_likelihood = ['{"rated likelihood":"N/A"}']


# imof = ImmigrationOfficer(resume)
# imof.evaluate_applicant()












