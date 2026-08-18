import os
import shutil
import django
from django.utils import timezone
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.conf import settings
from apps.news.models import NewsCategory, Post
from apps.core.models import JobDepartment, JobOpening

MEDIA_NEWS_DIR = os.path.join(settings.MEDIA_ROOT, "news")
os.makedirs(MEDIA_NEWS_DIR, exist_ok=True)

BRAIN_DIR = r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7"

NEWS_IMAGE_MAPPING = {
    "armena-wwtp-commissioning-operational-phase": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\news_armena_commissioning_1786893115576.jpg",
    "mostaqbal-misr-pipeline-milestone-completion": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\news_mostaqbal_misr_pipeline_1786893138794.jpg",
    "rural-sanitation-handover-assiut-minya-hayah-karima": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\news_hayah_karima_handover_1786893160608.jpg",
    "iso-9001-14001-45001-integrated-management-recertification": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\news_iso_certifications_1786893186360.jpg",
    "5-million-safe-man-hours-zero-lti-milestone": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\news_safety_milestone_1786893209279.jpg",
    "digital-construction-bim-3d-scada-deployment": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\news_bim_digital_twin_1786893235187.jpg",
}

# Copy News Images
for slug, src_path in NEWS_IMAGE_MAPPING.items():
    dest_filename = f"{slug}.jpg"
    dest_path = os.path.join(MEDIA_NEWS_DIR, dest_filename)
    if os.path.exists(src_path):
        shutil.copyfile(src_path, dest_path)
        print(f"Copied News Image: {src_path} -> {dest_path}")
    else:
        print(f"WARNING: Source image not found: {src_path}")

# ==========================================
# 1. SEED NEWS CATEGORIES & POSTS
# ==========================================
news_categories_data = [
    {"name": "Water & Sanitation", "slug": "water-sanitation"},
    {"name": "Strategic Infrastructure", "slug": "strategic-infrastructure"},
    {"name": "Municipal Networks", "slug": "municipal-networks"},
    {"name": "Corporate & Quality", "slug": "corporate-quality"},
    {"name": "Health, Safety & Environment", "slug": "health-safety-environment"},
    {"name": "Engineering & Innovation", "slug": "engineering-innovation"},
]

news_cat_objs = {}
for cat in news_categories_data:
    obj, _ = NewsCategory.objects.get_or_create(slug=cat["slug"], defaults={"name": cat["name"]})
    obj.name = cat["name"]
    obj.save()
    news_cat_objs[cat["slug"]] = obj

# Clear old posts
Post.objects.all().delete()

now = timezone.now()

posts_data = [
    {
        "title": "Armena Wastewater Treatment Plant in Aswan Enters Full Operational Phase with 15,000 m³/day Capacity",
        "slug": "armena-wwtp-commissioning-operational-phase",
        "category": news_cat_objs["water-sanitation"],
        "cover_image": "news/armena-wwtp-commissioning-operational-phase.jpg",
        "excerpt": "Al Bahaa Construction officially hands over the state-of-the-art Armena Wastewater Treatment Facility in Nasr El-Nuba, providing advanced biological treatment and sludge dewatering for Upper Egypt.",
        "content": (
            "Al Bahaa Construction (S.A.E) has officially announced the successful commissioning and operational handover of the Armena Wastewater Treatment Plant located in Nasr El-Nuba, Aswan Governorate. Developed under the auspices of the National Authority for Potable Water and Sanitary Drainage (NOPWASD), the landmark facility operates with a nominal daily treatment capacity of 15,000 cubic meters.\n\n"
            "The engineering execution encompassed turnkey civil, mechanical, and electrical installations. Key technical components include extended aeration biological basins, high-efficiency circular clarifiers, automated sludge thickening, mechanical screw press dewatering systems, and centralized SCADA automation.\n\n"
            "Eng. Executive Leadership highlighted that the treated effluent strictly complies with Egyptian environmental standards, safeguarding Nile basin groundwater reserves and supplying safe treated water for regional desert green belts and forestry projects."
        ),
        "published_at": now - timedelta(days=5),
        "is_published": True,
    },
    {
        "title": "Engineering Milestone: Completion and Pressure Testing of 2,500 mm PCCP Pipeline Section for Mostaqbal Misr",
        "slug": "mostaqbal-misr-pipeline-milestone-completion",
        "category": news_cat_objs["strategic-infrastructure"],
        "cover_image": "news/mostaqbal-misr-pipeline-milestone-completion.jpg",
        "excerpt": "Heavy engineering teams achieve successful hydrostatic pressure testing on giant 2.5-meter diameter pre-stressed concrete cylinder pipelines along the Dabaa agricultural corridor.",
        "content": (
            "Al Bahaa Construction has achieved a pivotal engineering milestone with the completion and hydrostatic pressure testing of its assigned section in the strategic Mostaqbal Misr Mega Water Conveyance Project along the Dabaa Corridor.\n\n"
            "The project entails the installation of giant 2,500 mm diameter Pre-stressed Concrete Cylinder Pipes (PCCP), designed to transport vast volumetric flows under high operating hydrostatic pressures across demanding desert geotechnical formations.\n\n"
            "Utilizing heavy crawler crane rigs, specialized laser-guided alignment, and robust thrust block stabilization, the engineering team executed the deep corridor trenching and joint sealing ahead of the scheduled project baseline, reinforcing the national agricultural reclamation agenda."
        ),
        "published_at": now - timedelta(days=14),
        "is_published": True,
    },
    {
        "title": "Accelerating Rural Sanitation: Handover of Networks in Assiut and Minya under Decent Life Initiative",
        "slug": "rural-sanitation-handover-assiut-minya-hayah-karima",
        "category": news_cat_objs["municipal-networks"],
        "cover_image": "news/rural-sanitation-handover-assiut-minya-hayah-karima.jpg",
        "excerpt": "Comprehensive sanitation infrastructure, gravity networks, and lifting pump stations across Eastern Al-Maabda, Manshaet Seif El-Nasr, and Beni Adyat enter active service.",
        "content": (
            "Under the transformative Decent Life (Hayah Karima) presidential initiative, Al Bahaa Construction has successfully handed over integrated municipal wastewater networks across multiple rural districts in Assiut and Minya Governorates.\n\n"
            "The combined scope delivered over 20 kilometers of uPVC and HDPE gravity collectors, reinforced concrete wet-well pumping stations, ductile iron force transmission pipelines, and thousands of domestic household hookups in Eastern Al-Maabda (Abnoub), Manshaet Seif El-Nasr (Mallawi), and Beni Adyat (Manfalout).\n\n"
            "This handover eliminates decades of environmental contamination, dramatically elevates local living standards, and ensures dependable connection to regional centralized purification plants."
        ),
        "published_at": now - timedelta(days=28),
        "is_published": True,
    },
    {
        "title": "Al Bahaa Construction Achieves Integrated Management System Recertification for ISO 9001, 14001, and 45001",
        "slug": "iso-9001-14001-45001-integrated-management-recertification",
        "category": news_cat_objs["corporate-quality"],
        "cover_image": "news/iso-9001-14001-45001-integrated-management-recertification.jpg",
        "excerpt": "International third-party audits reaffirm Al Bahaa's uncompromising standards in quality management, environmental sustainability, and occupational health and safety.",
        "content": (
            "Following comprehensive multi-site audit evaluations across head office operations and active infrastructure sites, Al Bahaa Construction has successfully renewed its certifications for ISO 9001:2015 (Quality Management), ISO 14001:2015 (Environmental Management), and ISO 45001:2018 (Occupational Health & Safety).\n\n"
            "The international audit panel commended Al Bahaa's standardized project delivery framework, rigorous subcontractor pre-qualification processes, and proactive environmental mitigation strategies.\n\n"
            "This renewal reflects the company's continuous investment in operational governance, digital documentation, and adherence to Grade A engineering standards."
        ),
        "published_at": now - timedelta(days=45),
        "is_published": True,
    },
    {
        "title": "Major Safety Milestone: Achieving 5 Million Safe Man-Hours Zero LTI Across Active Project Sites",
        "slug": "5-million-safe-man-hours-zero-lti-milestone",
        "category": news_cat_objs["health-safety-environment"],
        "cover_image": "news/5-million-safe-man-hours-zero-lti-milestone.jpg",
        "excerpt": "Rigorous site safety culture, hazard prevention protocols, and continuous daily toolbox talks culminate in 5,000,000 lost-time-incident-free working hours.",
        "content": (
            "Al Bahaa Construction is proud to celebrate reaching 5,000,000 consecutive safe man-hours without a Lost Time Incident (Zero LTI) across its portfolio of heavy civil, pipeline, and treatment plant projects.\n\n"
            "Executing complex deep-trench excavations exceeding 7 meters, high-tonnage pipe lifting, and live marine intake works involves high-risk environments. This achievement stands as a testament to the dedication of our HSE field officers, project managers, and entire workforce.\n\n"
            "The company marked the milestone with site recognition ceremonies honoring safety champions and reinforcing our core principle: every employee and contractor returns home safely every single day."
        ),
        "published_at": now - timedelta(days=60),
        "is_published": True,
    },
    {
        "title": "Digital Engineering Leadership: Full Deployment of 3D BIM & Telemetry Automation Across Active Projects",
        "slug": "digital-construction-bim-3d-scada-deployment",
        "category": news_cat_objs["engineering-innovation"],
        "cover_image": "news/digital-construction-bim-3d-scada-deployment.jpg",
        "excerpt": "Al Bahaa scales up digital twin modeling, automated clash detection, and IoT-enabled heavy machinery tracking to optimize constructability and project delivery timelines.",
        "content": (
            "As part of its ongoing strategic innovation roadmap, Al Bahaa Construction has fully integrated Building Information Modeling (BIM 3D/4D) and IoT telemetry into its technical office and field operations.\n\n"
            "By producing comprehensive digital twin models of complex piping, pump houses, and electromechanical chambers prior to on-site casting, multidisciplinary clash resolution times have been reduced by over 40%. Furthermore, real-time GPS telemetry across heavy earthmoving fleets optimizes fuel consumption and preventative maintenance schedules.\n\n"
            "This digital transformation ensures precision engineering, minimizes on-site material waste, and delivers transparent, data-driven reporting to project stakeholders and client authorities."
        ),
        "published_at": now - timedelta(days=75),
        "is_published": True,
    },
]

for p_data in posts_data:
    post, created = Post.objects.update_or_create(
        slug=p_data["slug"],
        defaults=p_data,
    )
    print(f"{'Created' if created else 'Updated'} Post: {post.title}")

# ==========================================
# 2. SEED JOB DEPARTMENTS & OPENINGS
# ==========================================
job_departments_data = [
    {"name": "Engineering & Projects", "slug": "engineering-projects", "order": 1},
    {"name": "Technical Office & BIM", "slug": "technical-office-bim", "order": 2},
    {"name": "Quality & Safety (QHSE)", "slug": "quality-safety", "order": 3},
    {"name": "Procurement & Supply Chain", "slug": "procurement-supply-chain", "order": 4},
]

dept_objs = {}
for dept in job_departments_data:
    obj, _ = JobDepartment.objects.get_or_create(slug=dept["slug"], defaults={"name": dept["name"], "order": dept["order"]})
    obj.name = dept["name"]
    obj.order = dept["order"]
    obj.save()
    dept_objs[dept["slug"]] = obj

# Clear old job openings
JobOpening.objects.all().delete()

jobs_data = [
    {
        "title": "Infrastructure Project Manager (Water & Wastewater Networks)",
        "slug": "infrastructure-project-manager-water-wastewater",
        "department": dept_objs["engineering-projects"],
        "location": "Upper Egypt Projects (Assiut / Minya)",
        "job_type": "Full-Time",
        "experience": "10-15 Years",
        "summary": "Lead the turnkey site execution of large-scale water transmission lines, gravity sewer networks, and wastewater pumping stations from site mobilization through to client commissioning.",
        "responsibilities": (
            "- Direct all on-site construction operations, subcontractors, and heavy machinery allocations\n"
            "- Ensure strict adherence to project baseline schedules, budget limits, and technical specifications\n"
            "- Interface with client consultant engineers (NOPWASD / Water Companies) for progress approvals\n"
            "- Manage project risk, variation orders, and resource forecasting across active work fronts"
        ),
        "requirements": (
            "- B.Sc. in Civil Engineering from an accredited university\n"
            "- Minimum 10 years of proven experience in municipal water and sewer network infrastructure\n"
            "- Strong background in deep trenching, dewatering, and pumping station civil works\n"
            "- PMP or equivalent project management credentials preferred"
        ),
        "benefits": (
            "- Highly competitive executive salary package\n"
            "- Comprehensive family medical and life insurance\n"
            "- Project completion performance bonuses\n"
            "- Company vehicle and site accommodation allowances"
        ),
        "is_active": True,
        "order": 1,
    },
    {
        "title": "Senior Site Civil Engineer (Pipelines & Deep Utilities)",
        "slug": "senior-site-civil-engineer-pipelines-utilities",
        "department": dept_objs["engineering-projects"],
        "location": "Site-Based (Upper Egypt / Greater Cairo)",
        "job_type": "Full-Time",
        "experience": "6-9 Years",
        "summary": "Supervise daily pipeline laying, trench excavation, manhole casting, and hydrostatic pressure testing for major water and sewerage conveyance lines.",
        "responsibilities": (
            "- Supervise daily pipe laying operations (HDPE, ductile iron, PCCP, and uPVC)\n"
            "- Enforce precision leveling, laser alignment, bedding, and compaction standards\n"
            "- Conduct hydrostatic pressure tests and joint integrity inspections with client consultants\n"
            "- Prepare daily site progress logs, material requests, and subcontractor work verification"
        ),
        "requirements": (
            "- B.Sc. in Civil Engineering\n"
            "- 6+ years of hands-on site execution experience in wet utilities and infrastructure\n"
            "- Proficiency in AutoCAD, total station surveying coordinates, and site documentation\n"
            "- Proven ability to lead site crews and enforce strict safety standards"
        ),
        "benefits": (
            "- Attractive site-based compensation package\n"
            "- Medical and life insurance coverage\n"
            "- Site allowances, transport, and rotation leaves"
        ),
        "is_active": True,
        "order": 2,
    },
    {
        "title": "Mechanical & Pumping Systems Project Engineer",
        "slug": "mechanical-pumping-systems-project-engineer",
        "department": dept_objs["engineering-projects"],
        "location": "Aswan / Nasr El-Nuba Projects",
        "job_type": "Full-Time",
        "experience": "5-8 Years",
        "summary": "Oversee the installation, alignment, and commissioning of electromechanical pumping equipment, valves, penstocks, and sludge treatment systems.",
        "responsibilities": (
            "- Manage the installation of submersible pumps, vertical turbine pumps, and split-case units\n"
            "- Supervise header piping, non-return check valves, surge vessels, and crane hoists\n"
            "- Coordinate with electrical engineers on MCC panel connections and SCADA telemetry\n"
            "- Lead pre-commissioning dry and wet testing protocols and handover documentation"
        ),
        "requirements": (
            "- B.Sc. in Mechanical Engineering\n"
            "- 5+ years experience in water/wastewater pump stations or treatment plant electromechanical works\n"
            "- Thorough knowledge of hydraulic equipment, pump curves, and alignment tolerances\n"
            "- Strong diagnostic and commissioning capabilities"
        ),
        "benefits": (
            "- Competitive monthly salary with hardship allowance\n"
            "- Medical insurance and annual performance bonus\n"
            "- Furnished accommodation and travel allowances"
        ),
        "is_active": True,
        "order": 3,
    },
    {
        "title": "Senior BIM & Infrastructure Modeling Engineer",
        "slug": "senior-bim-infrastructure-modeling-engineer",
        "department": dept_objs["technical-office-bim"],
        "location": "Headquarters - First Settlement, New Cairo",
        "job_type": "Full-Time",
        "experience": "4-7 Years",
        "summary": "Develop comprehensive 3D BIM models for civil infrastructure, pipe networks, and structural pump stations with multidisciplinary clash coordination.",
        "responsibilities": (
            "- Build federated 3D BIM models using Autodesk Revit and Civil 3D for utility networks\n"
            "- Execute Navisworks clash detection between civil, structural, and MEP piping models\n"
            "- Generate coordinated shop drawings, profiles, and detailed isometric pipe spool drawings\n"
            "- Extract precise quantities (QTO) directly from BIM models for procurement and billing"
        ),
        "requirements": (
            "- B.Sc. in Civil or Mechanical Engineering\n"
            "- Minimum 4 years in technical office BIM modeling for infrastructure or industrial projects\n"
            "- Mastery of Autodesk Revit, Civil 3D, Navisworks Manage, and BIM 360 / ACC\n"
            "- Certified BIM professional credential is a plus"
        ),
        "benefits": (
            "- Premium corporate salary\n"
            "- Comprehensive health insurance plan\n"
            "- Professional development and Autodesk certification sponsorship\n"
            "- Modern ergonomic corporate office environment"
        ),
        "is_active": True,
        "order": 4,
    },
    {
        "title": "Senior Tendering & Cost Estimation Engineer",
        "slug": "senior-tendering-cost-estimation-engineer",
        "department": dept_objs["technical-office-bim"],
        "location": "Headquarters - First Settlement, New Cairo",
        "job_type": "Full-Time",
        "experience": "6-10 Years",
        "summary": "Analyze tender documents, prepare accurate cost breakdowns, and formulate winning technical and financial proposals for national infrastructure bids.",
        "responsibilities": (
            "- Perform detailed quantity takeoffs from tender drawings and BOQs for civil & utility works\n"
            "- Solicit and analyze quotations from suppliers, equipment vendors, and subcontractors\n"
            "- Build comprehensive direct and indirect cost models including labor, plant, and materials\n"
            "- Prepare technical submission files, method statements, and risk assessment registers"
        ),
        "requirements": (
            "- B.Sc. in Civil Engineering\n"
            "- 6+ years experience in tendering and cost estimation within Grade A contracting firms\n"
            "- Deep understanding of FIDIC contract conditions and Egyptian public procurement laws\n"
            "- Advanced Excel modeling skills and familiarity with Candy (CCS) or Primavera"
        ),
        "benefits": (
            "- Highly rewarding compensation and annual bonus linked to tender awards\n"
            "- Medical and life insurance coverage\n"
            "- Career advancement opportunities in corporate management"
        ),
        "is_active": True,
        "order": 5,
    },
    {
        "title": "HSE Site Manager (Heavy Civil & Infrastructure)",
        "slug": "hse-site-manager-heavy-civil-infrastructure",
        "department": dept_objs["quality-safety"],
        "location": "Site-Based (Assiut / Minya / Aswan)",
        "job_type": "Full-Time",
        "experience": "7-10 Years",
        "summary": "Lead occupational health, safety, and environmental compliance across high-risk deep excavation, heavy lifting, and confined space operations.",
        "responsibilities": (
            "- Implement corporate HSE management systems aligned with ISO 45001 & ISO 14001\n"
            "- Conduct daily site safety inspections, risk assessments, and Job Safety Analyses (JSA)\n"
            "- Oversee safety protocols for deep trench shoring, crane lifting plans, and confined spaces\n"
            "- Lead safety toolbox talks, incident investigations, and client consultant HSE audits"
        ),
        "requirements": (
            "- B.Sc. in Engineering, Science, or relevant discipline\n"
            "- NEBOSH IGC certified (or OSHA Construction 30-Hour)\n"
            "- 7+ years HSE leadership experience on heavy civil/infrastructure construction sites\n"
            "- Strong communication and incident prevention track record"
        ),
        "benefits": (
            "- Competitive site-based remuneration package\n"
            "- Full medical insurance coverage\n"
            "- Site allowances and rotation leaves"
        ),
        "is_active": True,
        "order": 6,
    },
    {
        "title": "Senior QA/QC Materials & Civil Inspector",
        "slug": "senior-qa-qc-materials-civil-inspector",
        "department": dept_objs["quality-safety"],
        "location": "Project Sites (Greater Cairo / Upper Egypt)",
        "job_type": "Full-Time",
        "experience": "5-8 Years",
        "summary": "Ensure complete compliance with project quality plans, inspection and test plans (ITPs), and material approvals for reinforced concrete and pipeline works.",
        "responsibilities": (
            "- Inspect incoming materials (rebar, concrete batching, pipes, fittings) against approved submittals\n"
            "- Supervise laboratory sampling and testing (concrete cubes, soil compaction, pipe hydrotests)\n"
            "- Issue and track Requests for Inspection (RFIs) and manage non-conformance reports (NCRs)\n"
            "- Compile comprehensive QA/QC handover dossiers and manufacturer test certificates"
        ),
        "requirements": (
            "- B.Sc. in Civil Engineering\n"
            "- 5+ years QA/QC experience on infrastructure or commercial construction projects\n"
            "- Deep familiarity with Egyptian code requirements, ASTM, and BS standards\n"
            "- Detail-oriented with rigorous documentation capabilities"
        ),
        "benefits": (
            "- Attractive salary package\n"
            "- Medical and life insurance\n"
            "- Transportation and site allowances"
        ),
        "is_active": True,
        "order": 7,
    },
    {
        "title": "Senior Mechanical & Piping Procurement Specialist",
        "slug": "senior-mechanical-piping-procurement-specialist",
        "department": dept_objs["procurement-supply-chain"],
        "location": "Headquarters - First Settlement, New Cairo",
        "job_type": "Full-Time",
        "experience": "4-7 Years",
        "summary": "Source and procure high-spec piping, valves, pumps, electrical panels, and heavy construction equipment at optimal commercial terms.",
        "responsibilities": (
            "- Manage procurement cycles for infrastructure materials (ductile iron, HDPE, PCCP, valves)\n"
            "- Negotiate terms, pricing, and delivery schedules with local and international suppliers\n"
            "- Coordinate with site teams and logistics for timely delivery and customs clearance\n"
            "- Maintain vendor performance ratings and evaluate new pre-qualified suppliers"
        ),
        "requirements": (
            "- B.Sc. in Mechanical or Industrial Engineering\n"
            "- 4+ years procurement experience in heavy civil, MEP, or infrastructure contracting\n"
            "- Strong commercial negotiation and contract administration skills\n"
            "- Proficiency in ERP procurement modules (SAP / Oracle / Odoo)"
        ),
        "benefits": (
            "- Highly competitive salary and corporate benefits\n"
            "- Full medical and life insurance\n"
            "- Performance-based annual bonuses"
        ),
        "is_active": True,
        "order": 8,
    },
]

for j_data in jobs_data:
    job, created = JobOpening.objects.update_or_create(
        slug=j_data["slug"],
        defaults=j_data,
    )
    print(f"{'Created' if created else 'Updated'} Job: {job.title} ({job.department})")

print("\n--- Summary of Seeded News & Careers ---")
print(f"Total News Categories: {NewsCategory.objects.count()}")
print(f"Total Published Posts: {Post.objects.filter(is_published=True).count()}")
print(f"Total Job Departments: {JobDepartment.objects.count()}")
print(f"Total Active Jobs: {JobOpening.objects.filter(is_active=True).count()}")
