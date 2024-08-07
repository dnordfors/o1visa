import sys
from fastapi.testclient import TestClient
sys.path.append("..")

from app.main import app  # importing your FastAPI instance

client = TestClient(app)


def test_evaluate_resume():
    json_content = {
  "resume_content": "<h2><br></h2><h2>Personal Information</h2><p><strong>Name:</strong> xxxxxx</p><p><strong>Nationality:</strong> Hungarian</p><p><strong>Current Residence:</strong> Budapest, Hungary</p><p><strong>Contact:</strong> xxxxx</p><h2>Professional Summary</h2><p>Accomplished economist with over 20 years of experience in economic research, policy formulation, and academic teaching. Recognized globally for contributions to macroeconomic theory and policy analysis. Proven track record in advising governmental and international organizations on economic strategies and reforms. Fluent in Hungarian, English, and German.</p><h2>Education</h2><ul><li><strong>Ph.D. in Economics</strong> - Corvinus University of Budapest, Hungary (2003)</li><li><strong>M.A. in Economics</strong> - University of Szeged, Hungary (1998)</li><li><strong>B.A. in Economics</strong> - University of Szeged, Hungary (1996)</li></ul><h2>Professional Experience</h2><ul><li><strong>Senior Economic Advisor</strong> - Hungarian Ministry of Finance, Budapest, Hungary (2015-Present)</li><li class='ql-indent-1'>Advises on fiscal policy, economic reforms, and financial stability.</li><li class='ql-indent-1'>Leads economic research projects and drafts policy recommendations.</li><li class='ql-indent-1'>Represents Hungary in international economic forums.</li><li><strong>Professor of Economics</strong> - Corvinus University of Budapest, Hungary (2008-Present)</li><li class='ql-indent-1'>Teaches courses in macroeconomics, international economics, and economic policy.</li><li class='ql-indent-1'>Supervises doctoral research and theses.</li><li class='ql-indent-1'>Publishes research papers in leading economic journals.</li><li><strong>Research Fellow</strong> - Institute of Economics, Hungarian Academy of Sciences, Budapest, Hungary (2003-2015)</li><li class='ql-indent-1'>Conducted extensive research on macroeconomic stability and growth.</li><li class='ql-indent-1'>Collaborated with international research institutions on joint projects.</li><li class='ql-indent-1'>Presented findings at global economic conferences.</li></ul><h2>Publications</h2><ul><li>“Macroeconomic Stability in Emerging Markets” - Journal of Economic Perspectives (2020)</li><li>“Fiscal Policy and Economic Growth” - European Economic Review (2018)</li><li>“Globalization and Income Inequality” - World Development (2016)</li></ul><h2>Awards and Honors</h2><ul><li>Recipient of the Hungarian Academy of Sciences Award for Outstanding Research in Economics (2019)</li><li>Best Professor Award, Corvinus University of Budapest (2017)</li><li>Research Excellence Award, Institute of Economics, Hungarian Academy of Sciences (2014)</li></ul><h2>Languages</h2><ul><li>Hungarian (Native)</li><li>English (Fluent)</li><li>German (Fluent)</li></ul><h2>Professional Affiliations</h2><ul><li>Member, Hungarian Economic Association</li><li>Member, European Economic Association</li><li>Fellow, International Association for Applied Econometrics</li></ul><h2>References</h2><p>Available upon request</p><p>```</p>"
}


    response = client.post("/evaluate_resume", json=json_content)

    assert response.status_code == 200
    assert "assessment_report" in response.json()
    assert "letter_to_candidate" in response.json()
    assert "complete_dialogue_thread" in response.json()