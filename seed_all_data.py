import os
import django
from django.db import transaction
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.conf import settings
from apps.core.models import (
    AboutContent,
    AboutStatistic,
    CareerPillar,
    CareerSettings,
    ClientLogo,
    CompanyPillar,
    HomeContent,
    JobDepartment,
    JobOpening,
    PageHero,
    ServiceItem,
    SiteSettings,
    SpecializationItem,
    TeamMember,
    Testimonial,
)
from apps.news.models import NewsCategory, Post
from apps.projects.models import Project, ProjectCategory, ProjectImage


@transaction.atomic
def seed_everything():
    print("[INFO] Starting comprehensive standalone data seeding for Al Bahaa...")

    # Ensure media directories exist
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "branding"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "heroes"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "home"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "team"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "clients"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "testimonials"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "projects"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "news"), exist_ok=True)

    # 1. SiteSettings
    site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
    site_settings.company_name = "Al Bahaa Contracting (S.A.E)"
    site_settings.phone_main = "+20 (2) 2389 9255"
    site_settings.phone_tenders = "+20 (10) 0123 4567"
    site_settings.phone_sale = "+20 (2) 2389 9255"
    site_settings.phone_support = "+20 (10) 0123 4567"
    site_settings.email_general = "info@albahaacontracting.com"
    site_settings.email_tenders = "tenders@albahaacontracting.com"
    site_settings.email_careers = "careers@albahaacontracting.com"
    site_settings.email_sale = "info@albahaacontracting.com"
    site_settings.email_support = "tenders@albahaacontracting.com"
    site_settings.address_line1 = "Central Hub, Units 213-217"
    site_settings.address_line2 = "First Settlement, New Cairo, Egypt"
    site_settings.address = "Central Hub, Units 213-217, First Settlement, New Cairo, Egypt"
    site_settings.map_embed_url = "https://maps.google.com/maps?q=30.0633628,31.4215952+(Al+Bahaa+Contracting+-+Central+Hub)&t=&z=16&ie=UTF8&iwloc=&output=embed"
    site_settings.map_directions_url = "https://maps.app.goo.gl/wxBbUA5jU5uGwDTZ7"
    site_settings.working_hours_weekdays = "Sunday – Thursday: 8:00 AM – 5:00 PM"
    site_settings.working_hours_emergencies = "Friday & Saturday: Site Emergencies Only"
    site_settings.social_links = {
        "linkedin": "https://linkedin.com",
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
        "youtube": "https://youtube.com",
    }
    site_settings.footer_quote = "Established in 1986, AlBahaa delivers integrated contracting, finishing, and construction solutions across Egypt."
    site_settings.footer_quote_author = "Al Bahaa Contracting"
    site_settings.copyright_text = "(c) 2026 ALBAHAA CONSTRUCTION. ALL RIGHTS RESERVED"
    site_settings.save()
    print("[OK] SiteSettings seeded.")

    # 2. Page Heroes
    heroes_data = [
        {
            "page": "home",
            "eyebrow": "AL BAHAA CONTRACTING (S.A.E)",
            "title_line1": "ENGINEERING EXCELLENCE &",
            "title_line2": "CIVIL INFRASTRUCTURE",
            "description": "Established in 1986, Al Bahaa delivers Grade A water networks, turnkey civil construction, and enduring architectural landmarks across Egypt with disciplined execution.",
        },
        {
            "page": "about",
            "eyebrow": "About Al Bahaa",
            "title_line1": "We like to build",
            "title_line2": "things people use.",
            "description": "An Egyptian joint stock company with more than 30 years of engineering leadership, Grade A infrastructure classification, and turnkey project delivery.",
        },
        {
            "page": "projects",
            "eyebrow": "Featured Projects",
            "title_line1": "Built work",
            "title_line2": "with lasting value.",
            "description": "A focused collection of civil, administrative, and commercial infrastructure shaped with precision and engineered for long-term use.",
        },
        {
            "page": "news",
            "eyebrow": "NEWS & INSIGHTS",
            "title_line1": "Updated",
            "title_line2": "news.",
            "description": "Engineering milestones and technical updates across landmark projects.",
        },
        {
            "page": "careers",
            "eyebrow": "Careers",
            "title_line1": "Build what matters.",
            "title_line2": "",
            "description": "Join our multidisciplinary engineering teams to build landmark infrastructure projects across Egypt.",
        },
        {
            "page": "contact",
            "eyebrow": "Contact",
            "title_line1": "Let us talk",
            "title_line2": "about the next build.",
            "description": "Reach our engineering, tendering, and pre-construction teams for project inquiries, partnerships, and procurement.",
        },
    ]
    for h in heroes_data:
        hero_obj, _ = PageHero.objects.get_or_create(page=h["page"])
        hero_obj.eyebrow = h["eyebrow"]
        hero_obj.title_line1 = h["title_line1"]
        hero_obj.title_line2 = h["title_line2"]
        hero_obj.description = h["description"]
        hero_obj.save()
    print("[OK] PageHero banners seeded.")

    # 3. HomeContent & Specializations
    home_content, _ = HomeContent.objects.get_or_create(pk=1)
    home_content.blueprints_eyebrow = "OUR SPECIALIZATION"
    home_content.blueprints_title_line1 = "WE TURN BLUEPRINTS INTO"
    home_content.blueprints_title_line2 = "ENDURING REALITY."
    home_content.blueprints_description = "With more than three decades of engineering leadership and active membership in the Egyptian Federation for Construction, Al Bahaa delivers turnkey civil, residential, and infrastructure landmarks on schedule, within budget, and to the highest QA/QC standards."
    home_content.blueprints_btn_text = "View More"
    home_content.blueprints_btn_url = "/about/"
    home_content.save()

    specializations = [
        {
            "discipline": "GRADE A INFRASTRUCTURE",
            "title": "Municipal Water Transmission & Collector Networks",
            "description": "Specialized in municipal water transmission pipelines, sewage collector networks, pumping stations, and stormwater drainage systems engineered to exacting standards.",
            "order": 1,
        },
        {
            "discipline": "CIVIL & STRUCTURAL WORKS",
            "title": "Heavy Reinforced Concrete & Deep Foundations",
            "description": "Heavy reinforced concrete structures, deep foundation earthworks, structural steel framing, and institutional facilities built for enduring durability.",
            "order": 2,
        },
        {
            "discipline": "TURNKEY GENERAL CONTRACTING",
            "title": "Commercial & Residential Landmarks",
            "description": "Comprehensive end-to-end project execution from initial site earthworks and BIM coordination to high-end architectural finishes delivered on schedule.",
            "order": 3,
        },
        {
            "discipline": "ELECTROMECHANICAL & MEP",
            "title": "Integrated MEP, BMS & Substation Engineering",
            "description": "Advanced electro-mechanical installations, automated pump station control, value engineering, and high-efficiency MEP infrastructure.",
            "order": 4,
        },
    ]
    SpecializationItem.objects.all().delete()
    for s in specializations:
        SpecializationItem.objects.create(**s)
    print("[OK] HomeContent and Specializations seeded.")

    # 4. AboutContent, Statistics, Pillars, Services
    about_content, _ = AboutContent.objects.get_or_create(pk=1)
    about_content.who_we_are_title = "WHO WE ARE"
    about_content.who_we_are_p1 = "Albahaa Contracting is an Egyptian joint stock company (S.A.E) with more than 30 years of engineering and contracting experience. Established in 1986, Albahaa began its initial projects under the ownership of Engineer Mohamed Bahaa El Din Abdalla before formally transitioning into a joint stock company on December 14, 2000."
    about_content.who_we_are_p2 = "As an active member of the Egyptian Federation for Construction and Building Contractors since 1994, Albahaa holds the prestigious Grade A classification in water and sewage infrastructure networks, delivering turnkey civil, residential, and infrastructure landmarks on schedule and within budget."
    about_content.cta_eyebrow = "START A PROJECT"
    about_content.cta_title = "Ready to build something iconic?"
    about_content.cta_description = "Consult with our multidisciplinary engineering teams to bring technical precision and turnkey execution to your next landmark development."
    about_content.cta_primary_btn_text = "Contact Our Team"
    about_content.cta_primary_btn_url = "/contact/"
    about_content.cta_secondary_btn_text = "Explore Projects"
    about_content.cta_secondary_btn_url = "/projects/"
    about_content.save()

    statistics = [
        {"value": "30+", "label": "Years of Industry Experience (Est. 1986)", "order": 1},
        {"value": "Grade A", "label": "Water & Sewage Infrastructure Classification", "order": 2},
        {"value": "1994", "label": "Active Member, Egyptian Federation of Contractors", "order": 3},
        {"value": "S.A.E", "label": "Egyptian Joint Stock Enterprise (Inc. 2000)", "order": 4},
    ]
    AboutStatistic.objects.all().delete()
    for st in statistics:
        AboutStatistic.objects.create(**st)

    pillars = [
        {
            "number": "01",
            "title": "Technical Rigor & QA/QC",
            "description": "Leveraging state-of-the-art BIM modeling, advanced construction methods, and comprehensive QA/QC processes for flawless structural integrity.",
            "order": 1,
        },
        {
            "number": "02",
            "title": "Safety & Zero-Harm Protocol",
            "description": "Enforcing uncompromising occupational health and safety protocols across all active job sites, safeguarding our workforce and communities.",
            "order": 2,
        },
        {
            "number": "03",
            "title": "Sustainable Value Delivery",
            "description": "Integrating resource-efficient materials, lifecycle value engineering, and resilient construction practices built to endure for generations.",
            "order": 3,
        },
    ]
    CompanyPillar.objects.all().delete()
    for p in pillars:
        CompanyPillar.objects.create(**p)

    services = [
        {
            "title": "Water & Sewage Infrastructure (Grade A)",
            "description": "Extensive municipal water transmission mains, sewage collector networks, pumping stations, and stormwater drainage systems engineered to exacting standards.",
            "order": 1,
        },
        {
            "title": "Residential & Commercial Developments",
            "description": "Integrated residential communities, commercial hubs, and institutional headquarters delivered with disciplined execution and refined architectural finishes.",
            "order": 2,
        },
        {
            "title": "Turnkey Civil & General Contracting",
            "description": "Heavy civil works, deep foundation earthworks, structural concrete, and logistical infrastructure built for enduring durability.",
            "order": 3,
        },
        {
            "title": "Specialized MEP & Value Engineering",
            "description": "Advanced electro-mechanical installations, BIM coordination, stringent QA/QC protocols, and lifecycle cost optimization.",
            "order": 4,
        },
    ]
    ServiceItem.objects.all().delete()
    for s in services:
        ServiceItem.objects.create(**s)

    # 5. Team Members (Founder & Board)
    team_members = [
        {
            "name": "Eng. Mohamed Bahaa El Din Abdalla",
            "position": "Founder & Chairman",
            "member_type": "founder",
            "quote": "Building enduring engineering landmarks across Egypt with unwavering technical integrity.",
            "bio": "Beginning his career at Arab Contractors until 1978, he subsequently led regional operations as Regional Director in Medina at Aziz Company for Contracting and Industrial Investment. In 1986, he co-founded Albahaa Contracting, dedicating full executive leadership to establishing the company as one of Egypt's premier Grade A engineering and infrastructure enterprises.",
            "order": 1,
        },
        {
            "name": "Eng. Ahmed Bahaa",
            "position": "CEO / Board Member",
            "member_type": "executive",
            "quote": "Executing infrastructure with uncompromising technical rigor, punctuality, and fiscal responsibility.",
            "bio": "Leading executive engineering management, digital construction technologies, and nationwide project delivery.",
            "order": 2,
        },
        {
            "name": "Mr. Mahmoud Bahaa",
            "position": "Vice Chairman / Board Member",
            "member_type": "executive",
            "quote": "Building enduring partnerships through operational precision and transparent corporate governance.",
            "bio": "Directing corporate development, strategic client partnerships, and joint-stock operational excellence.",
            "order": 3,
        },
    ]
    TeamMember.objects.all().delete()
    for tm in team_members:
        TeamMember.objects.create(**tm)
    print("[OK] AboutContent, Statistics, Pillars, Services, and Leadership Team seeded.")

    # 6. Careers Settings & Pillars
    career_settings, _ = CareerSettings.objects.get_or_create(pk=1)
    career_settings.spontaneous_eyebrow = "SPONTANEOUS APPLICATION"
    career_settings.spontaneous_title = "Didn't find the right role for you?"
    career_settings.spontaneous_description = "We are constantly seeking passionate engineers, BIM coordinators, and construction managers. Send your CV and portfolio directly to our recruitment team, and we will contact you when a fitting opportunity opens."
    career_settings.spontaneous_btn_text = "Send Your CV"
    career_settings.spontaneous_email = "careers@albahaacontracting.com"
    career_settings.save()

    career_pillars = [
        {
            "number": "01",
            "title": "Engineering Precision",
            "description": "We take pride in executing complex engineering and construction challenges with uncompromising standards, modern methodologies, and meticulous attention to detail.",
            "order": 1,
        },
        {
            "number": "02",
            "title": "Safety & Culture",
            "description": "People come first. We maintain strict occupational health and safety protocols across all job sites while fostering an inclusive, collaborative team culture.",
            "order": 2,
        },
        {
            "number": "03",
            "title": "Career Growth",
            "description": "We invest in continuous learning, digital workflows, and leadership pathways to empower our professionals to build long-term, fulfilling careers.",
            "order": 3,
        },
    ]
    CareerPillar.objects.all().delete()
    for cp in career_pillars:
        CareerPillar.objects.create(**cp)

    # 7. Testimonials
    testimonials = [
        {
            "client_name": "Consulting Engineers Group (CEG)",
            "position": "Project Supervision",
            "company": "Major Urban Projects",
            "quote": "Al Bahaa's execution on major municipal infrastructure works demonstrated impeccable technical rigor, Grade A compliance, and flawless coordination.",
            "show_on_home": True,
            "show_on_about": True,
            "is_featured": True,
            "is_accent": False,
            "order": 1,
        },
        {
            "client_name": "Urban Communities Authority",
            "position": "Infrastructure Division",
            "company": "Ministry of Housing",
            "quote": "Their adherence to structural milestones, safety protocols, and quality control sets a benchmark for joint-stock contractors in Egypt.",
            "show_on_home": True,
            "show_on_about": True,
            "is_featured": True,
            "is_accent": False,
            "order": 2,
        },
        {
            "client_name": "Prime Developments",
            "position": "Executive Management",
            "company": "Commercial Real Estate",
            "quote": "Turnkey project delivery executed with superior craftsmanship, delivered on schedule with outstanding attention to engineering QA/QC.",
            "show_on_home": True,
            "show_on_about": True,
            "is_featured": True,
            "is_accent": True,
            "order": 3,
        },
    ]
    Testimonial.objects.all().delete()
    for t in testimonials:
        Testimonial.objects.create(**t)
    print("[OK] Career Settings, Pillars, and Testimonials seeded.")

    # 8. Client Logos
    client_logos = [
        {"name": "National Housing & Utilities Partner", "order": 1},
        {"name": "Urban Communities Authority", "order": 2},
        {"name": "Consulting Engineers Group (CEG)", "order": 3},
        {"name": "Prime Developments", "order": 4},
        {"name": "Civil Engineering Consultants", "order": 5},
        {"name": "Egyptian Federation for Construction", "order": 6},
    ]
    ClientLogo.objects.all().delete()
    for cl in client_logos:
        ClientLogo.objects.create(name=cl["name"], order=cl["order"], show_on_home=True, show_on_about=True)
    print("[OK] Client Logos seeded.")

    # 9. Job Departments & Openings
    departments_data = [
        {"name": "Site Engineering", "slug": "site-engineering", "order": 1},
        {"name": "Technical Office", "slug": "technical-office", "order": 2},
        {"name": "Quality Assurance & QC", "slug": "quality-assurance-qc", "order": 3},
        {"name": "MEP Operations", "slug": "mep-operations", "order": 4},
    ]
    dept_objs = {}
    for d in departments_data:
        obj, _ = JobDepartment.objects.get_or_create(slug=d["slug"], defaults={"name": d["name"], "order": d["order"]})
        obj.name = d["name"]
        obj.order = d["order"]
        obj.save()
        dept_objs[d["slug"]] = obj

    jobs_data = [
        {
            "title": "Senior Infrastructure Project Manager",
            "slug": "senior-infrastructure-project-manager",
            "department": dept_objs["site-engineering"],
            "location": "New Cairo / Assiut, Egypt",
            "job_type": "Full-Time",
            "experience": "10-15 Years",
            "summary": "Lead turnkey municipal water transmission mains, pump stations, and sewer network construction across multi-site developments.",
            "responsibilities": (
                "Direct site execution teams, subcontractors, and heavy machinery logistics in compliance with Grade A specifications.\n"
                "Supervise QA/QC compliance, hydrostatic pressure testing protocols, and client handover milestones.\n"
                "Manage project budgets, resource leveling, and procurement schedules via Primavera P6."
            ),
            "requirements": (
                "B.Sc. in Civil Engineering from an accredited university.\n"
                "Minimum 10 years experience in large-scale municipal water and sanitation networks.\n"
                "Proven leadership of multidisciplinary site engineering teams."
            ),
            "benefits": (
                "Competitive executive remuneration package.\n"
                "Company transportation or vehicle allowance.\n"
                "Comprehensive medical and life insurance coverage."
            ),
            "order": 1,
        },
        {
            "title": "Senior Technical Office & BIM Engineer",
            "slug": "senior-technical-office-bim-engineer",
            "department": dept_objs["technical-office"],
            "location": "Headquarters - New Cairo, Egypt",
            "job_type": "Full-Time",
            "experience": "6-9 Years",
            "summary": "Coordinate 3D BIM models (LOD 400), prepare structural shop drawings, clash detection reports, and quantity surveying submittals.",
            "responsibilities": (
                "Develop coordinated 3D BIM structural and civil infrastructure models utilizing Autodesk Revit and Navisworks.\n"
                "Prepare comprehensive structural shop drawings and bar bending schedules (BBS).\n"
                "Coordinate with consultant engineers for material submittal approvals and technical RFI resolutions."
            ),
            "requirements": (
                "B.Sc. in Civil or Structural Engineering.\n"
                "Expert proficiency in Revit Structure, AutoCAD, and Navisworks Manage.\n"
                "6+ years experience in technical office engineering for top-tier contracting firms."
            ),
            "benefits": (
                "Professional software training and certification subsidies.\n"
                "Performance-based annual project bonuses.\n"
                "Flexible modern corporate office environment."
            ),
            "order": 2,
        },
        {
            "title": "QA/QC Lead Engineer - Civil & Structural",
            "slug": "qa-qc-lead-engineer-civil-structural",
            "department": dept_objs["quality-assurance-qc"],
            "location": "Site Deployments - Greater Cairo & Minya",
            "job_type": "Full-Time",
            "experience": "7-10 Years",
            "summary": "Oversee inspection and testing plans (ITP), mass concrete thermal monitoring, and material validation across active projects.",
            "responsibilities": (
                "Enforce strict adherence to ISO 9001 quality management systems and Federation technical codes.\n"
                "Review concrete mix designs, slump verifications, and laboratory compressive strength test reports.\n"
                "Issue non-conformance reports (NCRs) and oversee root-cause corrective actions."
            ),
            "requirements": (
                "B.Sc. in Civil Engineering with certified QA/QC auditing credentials.\n"
                "7+ years in structural QA/QC for heavy civil, administrative towers, and infrastructure.\n"
                "Deep knowledge of ASTM, BS, and Egyptian Code of Practice (ECP)."
            ),
            "benefits": (
                "Site hardship allowances and performance incentives.\n"
                "Comprehensive medical insurance for employee and family.\n"
                "Career advancement pathways to QA/QC Directorate."
            ),
            "order": 3,
        },
        {
            "title": "Senior MEP Infrastructure Coordinator",
            "slug": "senior-mep-infrastructure-coordinator",
            "department": dept_objs["mep-operations"],
            "location": "Greater Cairo / Alexandria Desert Road",
            "job_type": "Full-Time",
            "experience": "8-12 Years",
            "summary": "Manage electro-mechanical installations, high-capacity pumping stations, medium-voltage substations, and automated telemetry.",
            "responsibilities": (
                "Supervise the installation, testing, and commissioning of heavy split-case pumps, surge vessels, and generator sets.\n"
                "Coordinate multidisciplinary MEP containment corridors and civil interfaces in BIM.\n"
                "Liaise with utility authorities for primary power connection approvals and energization protocols."
            ),
            "requirements": (
                "B.Sc. in Mechanical or Electrical Engineering.\n"
                "8+ years experience in pump station electromechanical works and large-diameter piping systems.\n"
                "Demonstrated track record of successful facility commissioning."
            ),
            "benefits": (
                "Attractive compensation package aligned with industry benchmarks.\n"
                "Full medical coverage and professional indemnity.\n"
                "Continuous technical training on automated SCADA and telemetry systems."
            ),
            "order": 4,
        },
    ]
    JobOpening.objects.all().delete()
    for j in jobs_data:
        JobOpening.objects.create(**j)
    print("[OK] Job Departments and Job Openings seeded.")

    # 10. Project Categories & Landmark Projects
    project_categories = [
        {"name": "Water & Wastewater Treatment", "slug": "water-wastewater-treatment", "order": 1},
        {"name": "Infrastructure & Utilities", "slug": "infrastructure-utilities", "order": 2},
        {"name": "Residential & Housing", "slug": "residential-housing", "order": 3},
        {"name": "Commercial & Corporate", "slug": "commercial-corporate", "order": 4},
    ]
    p_cat_objs = {}
    for pc in project_categories:
        obj, _ = ProjectCategory.objects.get_or_create(slug=pc["slug"], defaults={"name": pc["name"], "order": pc["order"]})
        obj.name = pc["name"]
        obj.order = pc["order"]
        obj.save()
        p_cat_objs[pc["slug"]] = obj

    projects_data = [
        {
            "title": "Eastern Al-Ma'abda Sewerage & Pumping Network",
            "slug": "eastern-al-maabda-sewerage",
            "category": p_cat_objs["water-wastewater-treatment"],
            "client_name": "National Authority for Potable Water & Sanitary Drainage (NOPWASD)",
            "status": "completed",
            "location": "Assiut Governorate, Egypt",
            "date": timezone.now().date(),
            "built_up_area": "34 km Collector Network",
            "scope_of_work": "Turnkey Sewerage Networks, Lift Station & Force Mains",
            "architect_consultant": "Consulting Engineers Group (CEG)",
            "short_description": "Turnkey execution of municipal wastewater collection networks, deep trench gravity lines, and a high-capacity lift station serving over 45,000 residents.",
            "full_description": (
                "The Eastern Al-Ma'abda Sewerage Project represents a flagship rural sanitation infrastructure landmark executed by Al Bahaa Contracting under the National Rural Sanitation Program.\n\n"
                "The engineering scope encompassed the construction of 34 kilometers of vitrified clay and uPVC gravity sewer pipelines ranging from 200mm to 600mm in diameter, installed at depths reaching 7.5 meters under complex geotechnical conditions.\n\n"
                "Works included a state-of-the-art wet-well pumping station equipped with dual submersible solids-handling pumps, automated bar screens, and an emergency diesel generator backup system."
            ),
            "engineering_highlights": (
                "Microtunneling and open-trench deep excavations with specialized dewatering in high water-table soils.\n"
                "HDPE force main pipeline installation with electrofusion welding and zero-leakage hydrostatic pressure testing.\n"
                "Integration of automated ultrasonic level sensors and remote SCADA monitoring telemetry."
            ),
            "sustainability": "Eliminated groundwater contamination risks and improved sanitary standards for over 45,000 rural residents.",
            "is_featured": True,
            "order": 1,
        },
        {
            "title": "Armena Wastewater Treatment Plant (WWTP)",
            "slug": "armena-wastewater-treatment-plant",
            "category": p_cat_objs["water-wastewater-treatment"],
            "client_name": "New Urban Communities Authority (NUCA)",
            "status": "completed",
            "location": "Aswan Governorate, Egypt",
            "date": timezone.now().date(),
            "built_up_area": "15,000 m3/day Capacity",
            "scope_of_work": "Civil Works, Biological Aeration Basins & Disinfection Facility",
            "architect_consultant": "Arab Consulting Engineers (ACE - Moharram Bakhoum)",
            "short_description": "Modern biological treatment plant with advanced primary sedimentation, extended aeration basins, chlorination facility, and treated effluent reuse infrastructure.",
            "full_description": (
                "Armena Wastewater Treatment Plant is a major environmental landmark engineered to deliver secondary and tertiary treated effluent for agricultural and green belt irrigation.\n\n"
                "Al Bahaa Contracting executed all reinforced concrete hydraulic structures, including intake equalization tanks, primary clarifiers, activated sludge oxidation ditches, and secondary sedimentation clarifiers.\n\n"
                "The plant was commissioned with automated dissolved oxygen control, mechanical surface aerators, and a fully equipped chemical laboratory."
            ),
            "engineering_highlights": (
                "High-durability sulfate-resistant concrete (SRC) formulation for all hydraulic water-retaining structures.\n"
                "Laser-guided mechanical scraper installation for zero-vibration clarifier operations.\n"
                "Turnkey electromechanical integration of blower rooms, chlorinators, and electrical MCC panels."
            ),
            "sustainability": "100% of treated wastewater repurposed for sustainable green landscaping and agricultural forestry.",
            "is_featured": True,
            "order": 2,
        },
        {
            "title": "Mostaqbal Misr Strategic Water Transmission Pipeline",
            "slug": "mostaqbal-misr-water-pipeline",
            "category": p_cat_objs["infrastructure-utilities"],
            "client_name": "Armed Forces Engineering Authority",
            "status": "completed",
            "location": "Dabaa Corridor / Western Desert, Egypt",
            "date": timezone.now().date(),
            "built_up_area": "42 km Line, 1400mm Diameter",
            "scope_of_work": "Ductile Iron & Pre-stressed Concrete Cylinder Pipe (PCCP)",
            "architect_consultant": "Military Technical College Consultancy Group",
            "short_description": "Large-diameter pressurized potable water transmission main supplying irrigation and developmental zones along the strategic Dabaa Axis.",
            "full_description": (
                "Part of Egypt's national food security and reclamation megaproject 'Mostaqbal Misr', this pipeline delivers vital bulk water supplies across demanding desert terrain.\n\n"
                "Al Bahaa mobilized heavy earthmoving fleets and automated pipe-laying equipment to complete 42 kilometers of 1400mm pipeline ahead of the mandated national deadline."
            ),
            "engineering_highlights": (
                "Cathodic protection against high-salinity desert subsurface soil conditions.\n"
                "Automatic air-release and surge anticipation valve chambers constructed at critical hydraulic crests.\n"
                "Strict adherence to 500,000 safe working hours with zero Lost Time Injuries (LTI)."
            ),
            "sustainability": "Provides life-sustaining irrigation water for thousands of acres of newly cultivated agricultural lands.",
            "is_featured": True,
            "order": 3,
        },
        {
            "title": "Dar Misr Residential Community - Phase II",
            "slug": "dar-misr-national-housing",
            "category": p_cat_objs["residential-housing"],
            "client_name": "Ministry of Housing & Urban Communities",
            "status": "completed",
            "location": "6th of October City, Egypt",
            "date": timezone.now().date(),
            "built_up_area": "64,000 m2 BUA - 32 Residential Buildings",
            "scope_of_work": "Turnkey General Contracting, Architecture & Internal Utilities",
            "architect_consultant": "Dar Al-Handasah Consultants",
            "short_description": "Integrated gated residential community comprising 32 luxury multi-story residential buildings, landscape plazas, and complete infrastructural utilities.",
            "full_description": (
                "Al Bahaa delivered 32 premium residential buildings under the Dar Misr National Housing Initiative, encompassing reinforced concrete skeletons, masonry, high-end interior finishes, and external utility connections.\n\n"
                "The project included dedicated parking areas, perimeter boundary walls, and modern stormwater drainage."
            ),
            "engineering_highlights": (
                "Optimized post-tensioned slab casting reducing structural execution cycles by 20%.\n"
                "Premium thermal insulation and double-glazed soundproof envelope systems.\n"
                "Integrated underground medium-voltage transformer stations and firefighting rings."
            ),
            "sustainability": "Energy-efficient architectural envelopes and water-saving sanitary fixtures.",
            "is_featured": True,
            "order": 4,
        },
        {
            "title": "Central Hub Administrative & Commercial Headquarters",
            "slug": "central-hub-headquarters",
            "category": p_cat_objs["commercial-corporate"],
            "client_name": "Al Bahaa Investment & Developments",
            "status": "completed",
            "location": "First Settlement, New Cairo, Egypt",
            "date": timezone.now().date(),
            "built_up_area": "18,500 m2 BUA - G+5 Floors",
            "scope_of_work": "Turnkey Architectural, Structural, Facade & BMS Integration",
            "architect_consultant": "Innovation Design Studio",
            "short_description": "Prime corporate administrative complex featuring unitized glass curtain wall facades, smart building automation, and high-efficiency MEP centralization.",
            "full_description": (
                "Central Hub serves as the corporate executive headquarters for Al Bahaa Contracting, alongside prime grade-A administrative and retail spaces in New Cairo.\n\n"
                "The building incorporates advanced building management systems (BMS), high-speed smart elevators, double-height executive lobbies, and underground automated multi-level parking."
            ),
            "engineering_highlights": (
                "Unitized double-glazed structural glass facade with low-E solar heat reduction coating.\n"
                "Central VRF climate control with energy-recovery ventilation units.\n"
                "Full NFPA-compliant firefighting and life safety system with intelligent smoke evacuation."
            ),
            "sustainability": "35% reduction in overall energy consumption through intelligent LED lighting and automated HVAC zoning.",
            "is_featured": True,
            "order": 5,
        },
    ]
    Project.objects.all().delete()
    for pr in projects_data:
        Project.objects.create(**pr)
    print("[OK] Project Categories and Landmark Projects seeded.")

    # 11. News Categories & Posts
    news_categories = [
        {"name": "Water & Sanitation", "slug": "water-sanitation", "order": 1},
        {"name": "Strategic Infrastructure", "slug": "strategic-infrastructure", "order": 2},
        {"name": "Civil Works", "slug": "civil-works", "order": 3},
        {"name": "Corporate & Quality", "slug": "corporate-quality", "order": 4},
        {"name": "Health, Safety & Environment", "slug": "health-safety-environment", "order": 5},
        {"name": "Engineering & Innovation", "slug": "engineering-innovation", "order": 6},
    ]
    n_cat_objs = {}
    for nc in news_categories:
        obj, _ = NewsCategory.objects.get_or_create(slug=nc["slug"], defaults={"name": nc["name"], "order": nc["order"]})
        obj.name = nc["name"]
        obj.order = nc["order"]
        obj.save()
        n_cat_objs[nc["slug"]] = obj

    posts_data = [
        {
            "title": "Advancing Egypt's Water & Municipal Transmission Networks",
            "slug": "advancing-egypts-water-infrastructure-networks",
            "category": n_cat_objs["water-sanitation"],
            "author": "Infrastructure Division",
            "published_at": timezone.now(),
            "excerpt": "Al Bahaa continues to expand its Grade A infrastructure division, executing critical municipal water transmission lines and automated pumping station networks engineered to exacting national QA/QC benchmarks.",
            "content": (
                "Across three decades of engineering leadership, Al Bahaa Contracting (S.A.E) has maintained an uncompromising commitment to executing Egypt's most critical civil and municipal infrastructure works.\n\n"
                "Our latest milestone encompasses the deployment of large-diameter ductile iron and HDPE water transmission mains, engineered with modern trenchless technology to minimize urban disruption while ensuring structural longevity.\n\n"
                "The engineering scope integrates multi-stage surge protection systems, cathodic protection against high-salinity subsurface conditions, and automated telemetry for real-time flow and pressure monitoring. With active Grade A classification from the Egyptian Federation for Construction, our teams adhere to the strictest quality assurance protocols from geotechnical excavation through to hydrostatic pressure testing."
            ),
            "is_published": True,
            "order": 1,
        },
        {
            "title": "Pioneering Quality Control & Structural Milestones in Civil Works",
            "slug": "pioneering-quality-control-structural-milestones",
            "category": n_cat_objs["civil-works"],
            "author": "Technical Office & QA/QC",
            "published_at": timezone.now(),
            "excerpt": "Achieving zero-defect concrete pours on high-capacity commercial and administrative structures through synchronized batch plant monitoring and thermal crack analysis.",
            "content": (
                "Mass concrete placement in demanding climate conditions requires rigorous thermal management and continuous monitoring. Al Bahaa's technical office recently delivered a milestone 3,200 m3 continuous raft foundation pour, utilizing low-heat Portland cement formulations combined with embedded thermocouple sensors.\n\n"
                "By implementing strict pre-pour mockups, digital slump verification, and temperature-controlled curing regimes, our structural engineering teams prevented thermal differential cracking while achieving target compressive strength well within standard curing cycles. This disciplined execution reinforces our reputation as a trusted partner for prime developments."
            ),
            "is_published": True,
            "order": 2,
        },
        {
            "title": "Sustainable High-Performance Facade Engineering in Modern Developments",
            "slug": "sustainable-high-performance-facade-engineering",
            "category": n_cat_objs["engineering-innovation"],
            "author": "Architectural Engineering Team",
            "published_at": timezone.now(),
            "excerpt": "Integrating climate-resilient envelope technologies and double-glazed curtain wall systems to optimize thermal performance across contemporary corporate headquarters.",
            "content": (
                "Contemporary architectural landmarks demand a harmonious balance between expressive geometric design and high-efficiency energy performance. Al Bahaa's architectural division specializes in engineering unitized curtain wall facades, acoustic barrier envelopes, and bespoke solar-shading louvers tailored to the climatic demands of Egypt.\n\n"
                "Our engineering methodology encompasses precise 3D BIM coordination, wind tunnel simulation validation, and on-site air/water infiltration testing to guarantee enduring envelope integrity and occupant comfort."
            ),
            "is_published": True,
            "order": 3,
        },
        {
            "title": "Turnkey Electromechanical & MEP Integration for Prime Landmarks",
            "slug": "turnkey-electromechanical-mep-integration",
            "category": n_cat_objs["strategic-infrastructure"],
            "author": "MEP Operations Division",
            "published_at": timezone.now(),
            "excerpt": "Delivering integrated firefighting, HVAC, substation distribution, and building management systems (BMS) with seamless architectural coordination.",
            "content": (
                "Complex landmark projects require seamless synchronization between heavy structural frameworks and sophisticated MEP systems. Al Bahaa provides comprehensive turnkey electromechanical solutions, from primary medium-voltage transformer stations and central chiller plants to intelligent automated building management systems (BMS).\n\n"
                "By coordinating multi-service containment corridors in BIM before field installation, our MEP teams eliminate on-site clashes, accelerate project schedules, and ensure long-term ease of maintenance for building operators."
            ),
            "is_published": True,
            "order": 4,
        },
        {
            "title": "Al Bahaa Achieves 5 Million Safe Man-Hours Zero-LTI Milestone",
            "slug": "5-million-safe-man-hours-zero-lti-milestone",
            "category": n_cat_objs["health-safety-environment"],
            "author": "HSE Directorate",
            "published_at": timezone.now(),
            "excerpt": "Marking an exceptional occupational health and safety milestone with five million continuous safe working hours without a single Lost Time Injury.",
            "content": (
                "Safety is not merely a protocol at Al Bahaa; it is our core corporate ethos. Our HSE directorate proudly announced the achievement of 5,000,000 safe man-hours without Lost Time Injury (LTI) across all active infrastructure and building construction sites in Egypt.\n\n"
                "This achievement reflects our comprehensive safety training programs, strict daily toolbox talks, rigorous scaffold inspections, and the unwavering commitment of our 1,200+ site personnel."
            ),
            "is_published": True,
            "order": 5,
        },
        {
            "title": "Integrated Management System ISO 9001, 14001 & 45001 Recertification",
            "slug": "iso-9001-14001-45001-integrated-management-recertification",
            "category": n_cat_objs["corporate-quality"],
            "author": "Executive Quality Committee",
            "published_at": timezone.now(),
            "excerpt": "Successfully completing the international recertification audit for Quality, Environmental, and Occupational Health & Safety Management Systems.",
            "content": (
                "Al Bahaa Contracting has successfully concluded its comprehensive surveillance and recertification audit for ISO 9001:2015 (Quality Management), ISO 14001:2015 (Environmental Management), and ISO 45001:2018 (Occupational Health and Safety).\n\n"
                "The certifying auditors highlighted our advanced digital quality control workflows, rigorous site environmental impact mitigations, and leadership-driven compliance as national benchmarks for joint-stock contracting enterprises."
            ),
            "is_published": True,
            "order": 6,
        },
    ]
    Post.objects.all().delete()
    for p in posts_data:
        Post.objects.create(**p)
    print("[OK] News Categories and Articles seeded.")

    print("[SUCCESS] All website content successfully seeded into database 100% dynamically!")


if __name__ == "__main__":
    seed_everything()
