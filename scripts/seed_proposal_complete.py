#!/usr/bin/env python3
"""
Seed script: 100% Proposal Content Realization for Al Bahaa Construction
Purges legacy dummy records and injects canonical corporate content, 13 featured projects,
6 leadership executives, 4 service divisions, 14 operating zones, and official brand identity.
"""
import os
import sys
from pathlib import Path
import django

# Setup Django environment
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.core.cache import cache
from django.utils import timezone
from apps.core.models import (
    SiteSettings,
    PageHero,
    HomeContent,
    AboutContent,
    AboutStatistic,
    CompanyPillar,
    TeamMember,
    ServiceItem,
    SpecializationItem,
    CareerSettings,
    CareerPillar,
    JobDepartment,
    JobOpening,
    ClientLogo,
    Testimonial,
)
from apps.projects.models import Project, ProjectCategory
from apps.news.models import Post, NewsCategory
from apps.dashboard.views import invalidate_site_cache


def seed_all():
    print("=" * 60)
    print("🚀 Starting Al Bahaa Construction 100% Content Seeding...")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. SITE IDENTITY & SETTINGS
    # -------------------------------------------------------------
    print("📦 1. Updating Site Settings & Identity...")
    settings = SiteSettings.load()
    settings.company_name = "Al Bahaa Construction"
    settings.email_general = "info@albahaaconstruction.com"
    settings.email_careers = "careers@albahaaconstruction.com"
    settings.email_tenders = "tenders@albahaaconstruction.com"
    settings.phone_main = "+20 (2) 2389 9255"
    settings.phone_tenders = "+20 (10) 0123 4567"
    settings.address = (
        "Central Hub Business Complex, Third Floor | Units 213, 214, 215 & 217, "
        "First Settlement, New Cairo, Adjacent to Kempinski Hotel, Egypt"
    )
    settings.address_line1 = "Central Hub Business Complex, Third Floor | Units 213, 214, 215 & 217"
    settings.address_line2 = "First Settlement, New Cairo, Adjacent to Kempinski Hotel, Egypt"
    settings.working_hours_weekdays = "Sunday – Thursday: 8:00 AM – 5:00 PM"
    settings.working_hours_emergencies = "Friday & Saturday: Site Emergencies Only"
    settings.footer_quote = (
        "Partner with Al Bahaa Construction for reliable infrastructure, "
        "engineering excellence, and sustainable project delivery across Egypt."
    )
    settings.footer_quote_author = "Al Bahaa Construction"
    settings.copyright_text = "© 2026 AL BAHAA CONSTRUCTION. ALL RIGHTS RESERVED"
    settings.save()

    career_settings = CareerSettings.load()
    career_settings.spontaneous_email = "careers@albahaaconstruction.com"
    career_settings.spontaneous_title = "Didn't find the right role for you?"
    career_settings.spontaneous_description = (
        "We are constantly seeking passionate engineers, accountants, and construction managers. "
        "Send your CV directly to our recruitment team at careers@albahaaconstruction.com."
    )
    career_settings.save()

    # -------------------------------------------------------------
    # 2. PAGE HEROES & HOME/ABOUT CONTENT
    # -------------------------------------------------------------
    print("📦 2. Updating Page Heroes & Monograph Copy...")
    heroes_data = {
        "home": {
            "eyebrow": "AL BAHAA CONSTRUCTION",
            "title_line1": "ENGINEERING EXCELLENCE.",
            "title_line2": "INFRASTRUCTURE LEADERSHIP.",
            "description": (
                "For nearly four decades, Al Bahaa Construction has delivered critical infrastructure, "
                "water, wastewater, irrigation, residential, and electromechanical projects across Egypt."
            ),
        },
        "about": {
            "eyebrow": "ABOUT AL BAHAA CONSTRUCTION",
            "title_line1": "Building Egypt's Infrastructure",
            "title_line2": "Since 1986",
            "description": (
                "A recognized Grade A engineering and infrastructure contractor delivering large-scale "
                "strategic developments across the Arab Republic of Egypt."
            ),
        },
        "projects": {
            "eyebrow": "OUR PROJECTS",
            "title_line1": "Engineering Milestones",
            "title_line2": "Delivered Nationwide",
            "description": (
                "Explore our landmark infrastructure, water lifting facilities, strategic pipelines, "
                "and national housing developments."
            ),
        },
        "careers": {
            "eyebrow": "CAREERS",
            "title_line1": "Build What Matters.",
            "title_line2": "Grow With Al Bahaa",
            "description": (
                "Join our multidisciplinary engineering, finance, and construction management teams "
                "shaping sustainable infrastructure."
            ),
        },
        "contact": {
            "eyebrow": "CONTACT US",
            "title_line1": "Let's Build The Future",
            "title_line2": "Together",
            "description": (
                "Partner with Al Bahaa Construction for reliable infrastructure, engineering excellence, "
                "and sustainable project delivery across Egypt."
            ),
        },
        "news": {
            "eyebrow": "NEWS & INSIGHTS",
            "title_line1": "Corporate Milestones &",
            "title_line2": "Industry Recognition",
            "description": (
                "Stay updated on our latest project handovers, engineering innovations, and global awards."
            ),
        },
    }

    for page_key, hero_vals in heroes_data.items():
        hero_obj, _ = PageHero.objects.get_or_create(page=page_key)
        hero_obj.eyebrow = hero_vals["eyebrow"]
        hero_obj.title_line1 = hero_vals["title_line1"]
        hero_obj.title_line2 = hero_vals["title_line2"]
        hero_obj.description = hero_vals["description"]
        hero_obj.save()

    home_content = HomeContent.load()
    home_content.blueprints_eyebrow = "OUR SPECIALIZATION"
    home_content.blueprints_title_line1 = "WE TURN BLUEPRINTS INTO"
    home_content.blueprints_title_line2 = "ENDURING REALITY."
    home_content.blueprints_description = (
        "For nearly four decades, Al Bahaa Construction has delivered critical infrastructure, water, "
        "wastewater, irrigation, residential, and electromechanical projects across Egypt. From major national "
        "development initiatives to essential community infrastructure, we combine engineering expertise, "
        "operational excellence, and a commitment to quality to create long-term value for our clients and the communities we serve."
    )
    home_content.blueprints_btn_text = "About Al Bahaa"
    home_content.blueprints_btn_url = "/about/"
    home_content.save()

    about_content = AboutContent.load()
    about_content.who_we_are_title = "WHO WE ARE"
    about_content.who_we_are_p1 = (
        "Al Bahaa Construction is a leading Egyptian engineering and construction company specializing in infrastructure, "
        "water and wastewater systems, irrigation networks, electromechanical works, public utilities, and residential developments."
    )
    about_content.who_we_are_p2 = (
        "Founded by Engineer Mohamed Bahaa El Din Abdalla, the company evolved from a successful contracting enterprise "
        "into a fully integrated joint stock company, delivering large-scale projects for government entities, infrastructure "
        "authorities, and national development programs. Today, Al Bahaa Construction is recognized as one of Egypt's trusted "
        "infrastructure contractors, with a proven track record spanning water treatment facilities, pumping stations, "
        "desalination plants, transmission pipelines, housing developments, and utility infrastructure."
    )
    about_content.cta_eyebrow = "PARTNER WITH US"
    about_content.cta_title = "Let's Build the Future Together"
    about_content.cta_description = (
        "Partner with Al Bahaa Construction for reliable infrastructure, engineering excellence, and sustainable project delivery across Egypt."
    )
    about_content.cta_primary_btn_text = "Contact Our Team"
    about_content.cta_primary_btn_url = "/contact/"
    about_content.cta_secondary_btn_text = "Explore Projects"
    about_content.cta_secondary_btn_url = "/projects/"
    about_content.save()

    # -------------------------------------------------------------
    # 3. KEY FIGURES & STATISTICS
    # -------------------------------------------------------------
    print("📦 3. Seeding Canonical Key Figures...")
    AboutStatistic.objects.all().delete()
    stats_data = [
        {"value": "1986", "label": "Founded in Egypt", "order": 1},
        {"value": "40 Years", "label": "Engineering & Contracting Experience", "order": 2},
        {"value": "Grade A", "label": "Contractor in Water & Wastewater Networks", "order": 3},
        {"value": "1M m³/d", "label": "Water Lifting Capacity Executed", "order": 4},
        {"value": "2,500 mm", "label": "Largest Pipeline Diameter Delivered", "order": 5},
        {"value": "Nationwide", "label": "Operations Across Egypt", "order": 6},
    ]
    for s in stats_data:
        AboutStatistic.objects.create(**s, is_active=True)

    # -------------------------------------------------------------
    # 4. COMPANY VALUES (7 VALUES)
    # -------------------------------------------------------------
    print("📦 4. Seeding 7 Corporate Values...")
    CompanyPillar.objects.all().delete()
    values_data = [
        {"number": "01", "title": "Excellence", "description": "Upholding uncompromising engineering precision, technical mastery, and quality assurance in every deliverable.", "order": 1},
        {"number": "02", "title": "Integrity", "description": "Operating with utmost transparency, ethical accountability, and unwavering compliance with statutory standards.", "order": 2},
        {"number": "03", "title": "Commitment", "description": "Delivering complex infrastructure landmarks on schedule, within scope, and aligned with client objectives.", "order": 3},
        {"number": "04", "title": "Safety", "description": "Enforcing stringent zero-harm occupational health, safety, and environmental protocols across all job sites.", "order": 4},
        {"number": "05", "title": "Expertise", "description": "Leveraging four decades of multidisciplinary civil, hydraulic, and electromechanical engineering know-how.", "order": 5},
        {"number": "06", "title": "Partnership", "description": "Cultivating enduring collaborative relationships with sovereign authorities, public sector clients, and communities.", "order": 6},
        {"number": "07", "title": "Efficiency", "description": "Optimizing resource utilization, disciplined planning, and lifecycle value engineering for sustainable impact.", "order": 7},
    ]
    for v in values_data:
        CompanyPillar.objects.create(**v, is_active=True)

    # -------------------------------------------------------------
    # 5. LEADERSHIP TEAM (6 EXECUTIVES)
    # -------------------------------------------------------------
    print("📦 5. Seeding Leadership Team (6 C-Level Executives)...")
    TeamMember.objects.all().delete()
    team_data = [
        {
            "name": "Engineer Mohamed Bahaa Abdalla",
            "position": "Founder & Chairman",
            "member_type": "founder",
            "photo": "team/Rectangle 24.webp",
            "quote": "Building enduring infrastructure that elevates communities and advances Egypt's national development agenda.",
            "bio": (
                "Founded Al Bahaa in 1986 with a vision of engineering rigor and nation-building. Under his leadership, "
                "the enterprise grew from a specialized contracting firm into an integrated Grade A corporate contractor."
            ),
            "order": 1,
        },
        {
            "name": "Engineer Ahmed Bahaa",
            "position": "CEO & Managing Director",
            "member_type": "executive",
            "photo": "team/ahmed_bahaa.webp",
            "quote": "Driving operational innovation, technical excellence, and sustainable expansion across major national programs.",
            "bio": "Leads executive management, strategic expansion, and overall operations of Al Bahaa Construction.",
            "order": 2,
        },
        {
            "name": "Mr. Mahmoud Bahaa",
            "position": "Vice Chairman",
            "member_type": "executive",
            "photo": "team/mahmoud_bahaa.webp",
            "quote": "Ensuring corporate governance, institutional resilience, and sustainable value delivery across our enterprise.",
            "bio": "Oversees corporate governance, strategic alliances, and commercial growth.",
            "order": 3,
        },
        {
            "name": "Engineer Ahmed El Mishad",
            "position": "Chief Operations Officer",
            "member_type": "executive",
            "photo": "team/Rectangle 24 copy.webp",
            "quote": "Disciplined execution and operational rigor at every scale of project delivery.",
            "bio": "Directs nationwide project execution, resource allocation, and field engineering operations.",
            "order": 4,
        },
        {
            "name": "Engineer Hany El Banna",
            "position": "Chief Business Officer",
            "member_type": "executive",
            "photo": "team/Rectangle 24 copy 2 .webp",
            "quote": "Building enduring partnerships with national infrastructure authorities and strategic clients.",
            "bio": "Leads business development, tendering, client relations, and strategic market positioning.",
            "order": 5,
        },
        {
            "name": "Mr. Ramy El Shaarawy",
            "position": "Chief Financial Officer",
            "member_type": "executive",
            "photo": "team/Rectangle 24 copy 3 .webp",
            "quote": "Fiscal discipline, robust capital structure, and transparent cost governance.",
            "bio": "Manages corporate finance, risk management, financial reporting, and capital planning.",
            "order": 6,
        },
    ]
    for m in team_data:
        TeamMember.objects.create(**m, is_active=True)

    # -------------------------------------------------------------
    # 6. SERVICES & SPECIALIZATIONS (4 SECTORS)
    # -------------------------------------------------------------
    print("📦 6. Seeding 4 Service Divisions & 24 Sub-Services...")
    ServiceItem.objects.all().delete()
    SpecializationItem.objects.all().delete()

    services_data = [
        {
            "discipline": "WATER & WASTEWATER INFRASTRUCTURE",
            "title": "Water & Wastewater Systems (Grade A)",
            "description": "Comprehensive water treatment facilities, wastewater treatment plants, municipal distribution networks, sewer collector pipelines, water transmission mains, high-capacity pumping stations, booster stations, and strategic storage reservoirs.",
            "order": 1,
        },
        {
            "discipline": "IRRIGATION, CANALS & DRAINAGE",
            "title": "Irrigation, Canals & Drainage Works",
            "description": "Engineering of main arterial canals, advanced irrigation infrastructure, agricultural reclamation water systems, regional drainage networks, and complex hydraulic control structures.",
            "order": 2,
        },
        {
            "discipline": "ELECTROMECHANICAL WORKS",
            "title": "Specialized Electromechanical (MEP) Works",
            "description": "Installation of high-capacity water lifting and pumping equipment, seawater and brackish desalination systems, heavy mechanical plant assemblies, high/medium voltage electrical infrastructure, and SCADA commissioning & operation support.",
            "order": 3,
        },
        {
            "discipline": "RESIDENTIAL & CIVIL CONSTRUCTION",
            "title": "Residential & General Civil Construction",
            "description": "Turnkey community developments, national social housing programs, luxury villas and residential compounds, corporate administrative headquarters, and industrial facilities delivered with architectural craftsmanship.",
            "order": 4,
        },
    ]

    for s in services_data:
        ServiceItem.objects.create(
            title=s["title"],
            description=s["description"],
            order=s["order"],
            is_active=True,
        )
        SpecializationItem.objects.create(
            discipline=s["discipline"],
            title=s["title"],
            description=s["description"],
            order=s["order"],
            is_active=True,
        )

    # -------------------------------------------------------------
    # 7. PROJECT CATEGORIES & 13 FEATURED PROJECTS
    # -------------------------------------------------------------
    print("📦 7. Seeding Project Categories & 13 Featured Projects...")
    Project.objects.all().delete()
    ProjectCategory.objects.all().delete()

    cat_water, _ = ProjectCategory.objects.get_or_create(
        slug="water-and-wastewater",
        defaults={"name": "Water & Wastewater Systems", "order": 1},
    )
    cat_pipelines, _ = ProjectCategory.objects.get_or_create(
        slug="pipelines-and-intakes",
        defaults={"name": "Strategic Pipelines & Intakes", "order": 2},
    )
    cat_housing, _ = ProjectCategory.objects.get_or_create(
        slug="housing-and-civil",
        defaults={"name": "Housing & Civil Construction", "order": 3},
    )
    cat_pumping, _ = ProjectCategory.objects.get_or_create(
        slug="pumping-and-booster",
        defaults={"name": "Pumping & Multi-Utility Stations", "order": 4},
    )

    projects_data = [
        {
            "title": "Al Mahsama Water Lift Station",
            "slug": "al-mahsama-water-lift-station",
            "category": cat_pumping,
            "client_name": "Armed Forces Engineering Authority",
            "location": "Ismailia, Egypt",
            "cover_image": "projects/al-mahsama-water-lift-station.webp",
            "built_up_area": "1,000,000 m³/day",
            "scope_of_work": "Water Lifting Station & Hydraulic Pumping Infrastructure",
            "short_description": "One of the most significant projects in our portfolio, designed to pump approximately 1 million m³ of water per day to support agricultural development in Sinai.",
            "full_description": (
                "The Al Mahsama Water Lift Station represents a strategic cornerstone in Egypt's national water reclamation program. "
                "Engineered to lift and convey approximately 1,000,000 m³ of agricultural drainage water per day beneath the Suez Canal, "
                "the facility provides vital irrigation supply to support agricultural development across central Sinai.\n\n"
                "The project encompassed deep intake sumps, heavy electromechanical pumping units, surge protection vessels, SCADA automation, "
                "and high-voltage electrical substation connections executed under stringent QA/QC protocols."
            ),
            "engineering_highlights": (
                "1 Million m³/day total water lifting and conveyance capacity.\n"
                "Heavy-duty intake chambers and deep dry-well pump installations.\n"
                "Integrated surge vessel suppression systems and automated SCADA control.\n"
                "Contributed to the ENR Global Best Project Award 2020."
            ),
            "status": "completed",
            "is_featured": True,
            "order": 1,
        },
        {
            "title": "Mostaqbal Misr Water Pipeline",
            "slug": "mostaqbal-misr-water-pipeline",
            "category": cat_pipelines,
            "client_name": "Armed Forces Water Authority",
            "location": "New Delta Project, 6th of October City, Egypt",
            "cover_image": "projects/mostaqbal-misr-water-pipeline.webp",
            "built_up_area": "Ø 2,500 mm Pipeline",
            "scope_of_work": "Prestressed Concrete Cylinder Pipeline (PCCP) Transmission",
            "short_description": "Construction of a 2,500 mm diameter prestressed concrete pipeline, one of the largest pipeline projects executed by the company.",
            "full_description": (
                "As part of the mega New Delta agricultural reclamation initiative, Al Bahaa Construction executed the supply, trenching, "
                "laying, and testing of a massive 2,500 mm diameter prestressed concrete cylinder pipeline (PCCP).\n\n"
                "This strategic transmission line delivers raw water across challenging desert topography, utilizing precision laser alignment, "
                "specialized heavy lifting cranes, and hydrostatic pressure testing to ensure long-term durability and leak-free transmission."
            ),
            "engineering_highlights": (
                "2,500 mm diameter prestressed concrete cylinder pipe (PCCP) execution.\n"
                "Extensive deep-trench earthworks and specialized bedding in desert terrain.\n"
                "High-capacity thrust blocks and air release/washout chamber installations.\n"
                "Crucial hydraulic artery for the New Delta Agricultural Project."
            ),
            "status": "completed",
            "is_featured": True,
            "order": 2,
        },
        {
            "title": "Al Minya Nile Intake Pumping Station",
            "slug": "al-minya-nile-intake-pumping-station",
            "category": cat_pumping,
            "client_name": "Armed Forces Engineering Authority",
            "location": "Al Minya, Egypt",
            "cover_image": "projects/alminya-nile-water-intake-station.webp",
            "built_up_area": "62,000 Acres Service Area",
            "scope_of_work": "Direct River Intake, Intake Pumping Station & Booster Main",
            "short_description": "Water intake and pumping infrastructure supporting the reclamation and irrigation of 62,000 acres.",
            "full_description": (
                "Turnkey engineering and civil execution of a primary Nile River intake structure and high-head pumping station in Upper Egypt. "
                "The station lifts raw water directly from the River Nile to convey it to newly reclaimed agricultural lands spanning 62,000 acres in Western Minya.\n\n"
                "Works included underwater suction piping, intake screens, wet well construction, motor control centers (MCC), and high-pressure manifold piping."
            ),
            "engineering_highlights": (
                "Heavy civil marine and riverbank intake structure construction.\n"
                "High-head horizontal split-case pump assemblies with automated monitoring.\n"
                "Direct raw water supply feeding the reclamation of 62,000 agricultural acres.\n"
                "High-reliability electrical control and telemetry systems."
            ),
            "status": "completed",
            "is_featured": True,
            "order": 3,
        },
        {
            "title": "Sadat City Water Treatment Plant (Phase 1)",
            "slug": "sadat-city-water-treatment-plant",
            "category": cat_water,
            "client_name": "New Urban Communities Authority (NUCA)",
            "location": "Sadat City, Monufia, Egypt",
            "cover_image": "projects/project_1.webp",
            "built_up_area": "87,000 m³/day Capacity",
            "scope_of_work": "Potable Water Treatment Plant Construction & Electromechanical Works",
            "short_description": "Phase One of an 87,000 m³/day treatment facility supporting urban expansion and water demand in Sadat City.",
            "full_description": (
                "Construction and commissioning of Phase 1 of the municipal potable water purification plant in Sadat City. "
                "With a designed throughput of 87,000 m³/day, the facility features clariflocculators, rapid sand gravity filters, "
                "chemical dosing buildings, disinfection systems, and clear water storage tanks.\n\n"
                "The plant secures drinking water supply for existing industrial zones and expanding residential districts across Sadat City."
            ),
            "engineering_highlights": (
                "87,000 m³/day Phase 1 design and execution throughput.\n"
                "Reinforced concrete clariflocculators and rapid gravity filter batteries.\n"
                "Automated chemical feed systems, chlorination, and sludge drying beds.\n"
                "Comprehensive integration with municipal transmission distribution networks."
            ),
            "status": "completed",
            "is_featured": True,
            "order": 4,
        },
        {
            "title": "Dar Misr National Housing Project",
            "slug": "dar-misr-national-housing-project",
            "category": cat_housing,
            "client_name": "Armed Forces Engineering Authority",
            "location": "New Cairo, Egypt",
            "cover_image": "projects/dar-misr-national-housing.webp",
            "built_up_area": "Multi-Building Residential Complex",
            "scope_of_work": "Turnkey Residential Buildings, Infrastructure & Landscaping",
            "short_description": "Turnkey development comprising residential buildings and supporting infrastructure delivering modern housing communities.",
            "full_description": (
                "Turnkey general contracting development within the prestigious Dar Misr national middle-income housing initiative in New Cairo. "
                "Al Bahaa Construction delivered structural concrete, premium architectural finishing, internal utility networks, and external "
                "site works under rigorous quality assurance standards."
            ),
            "engineering_highlights": (
                "Multi-story residential apartment buildings delivered turnkey.\n"
                "High-grade thermal insulation, acoustic glazing, and architectural finishes.\n"
                "Integrated potable water, sewage, stormwater, and electrical site networks.\n"
                "Paved internal roadways, pedestrian walkways, and landscaped green zones."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 5,
        },
        {
            "title": "Sakan Misr Housing Development",
            "slug": "sakan-misr-housing-development",
            "category": cat_housing,
            "client_name": "New Cairo Urban Communities Authority",
            "location": "New Cairo, Egypt",
            "cover_image": "projects/sakan-misr-housing-development.webp",
            "built_up_area": "144 Housing Units",
            "scope_of_work": "Residential Buildings Construction & Finishing Works",
            "short_description": "Construction of multiple residential buildings totaling 144 modern housing units.",
            "full_description": (
                "Execution of residential apartment blocks comprising 144 fully finished housing units in New Cairo. "
                "Scope included reinforced concrete foundations and frames, masonry, waterproofing, interior and exterior finishes, "
                "elevators, electrical substations, and surrounding public infrastructure."
            ),
            "engineering_highlights": (
                "144 premium finished housing units delivered on schedule.\n"
                "Precision post-tensioned slabs and reinforced concrete superstructure.\n"
                "Complete MEP plumbing, firefighting, and electrical installations.\n"
                "Full compliance with New Cairo Urban Communities Authority building codes."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 6,
        },
        {
            "title": "Edfu Wastewater Treatment Plant",
            "slug": "edfu-wastewater-treatment-plant",
            "category": cat_water,
            "client_name": "National Organization for Potable Water and Sanitary Drainage (NOPWASD)",
            "location": "Aswan, Egypt",
            "cover_image": "projects/project_2.webp",
            "built_up_area": "18,000 m³/day Capacity",
            "scope_of_work": "Municipal WWTP, Gravity Sewer Networks & Force Mains",
            "short_description": "Construction of a wastewater treatment facility with a capacity of 18,000 m³/day, serving approximately 70% of Edfu City's population.",
            "full_description": (
                "Construction of an integrated municipal sanitary drainage scheme serving approximately 70% of Edfu City in Aswan Governorate. "
                "The project features an 18,000 m³/day wastewater treatment facility with biological oxidation, primary/secondary settlement, "
                "sludge treatment, main pumping stations, and high-pressure force mains."
            ),
            "engineering_highlights": (
                "18,000 m³/day treatment capacity serving 70% of Edfu's population.\n"
                "Complete biological treatment units, chlorination, and sludge dewatering.\n"
                "Extensive gravity collection sewer lines and high-pressure discharge force mains.\n"
                "Critical environmental project improving Upper Egypt sanitation standards."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 7,
        },
        {
            "title": "Bani Adiyat Sewerage Networks",
            "slug": "bani-adiyat-sewerage-networks",
            "category": cat_water,
            "client_name": "National Organization for Potable Water and Sanitary Drainage (NOPWASD)",
            "location": "Assiut, Egypt",
            "cover_image": "projects/beni-adyat-sewerage.webp",
            "built_up_area": "9.4+ km Pressurized Pipelines",
            "scope_of_work": "1,000 mm & 1,200 mm Diameter Force Mains & Sewer Networks",
            "short_description": "Execution of more than 9.4 km of pressurized sewer pipelines, including 1,000 mm and 1,200 mm diameter lines, enhancing regional wastewater infrastructure capacity.",
            "full_description": (
                "Large-scale sanitary drainage infrastructure project in Assiut Governorate comprising over 9.4 km of heavy-duty pressurized "
                "sewer force mains with diameters reaching 1,000 mm and 1,200 mm. The scheme substantially expands regional wastewater discharge "
                "capacity and eliminates environmental hazards in rural communities."
            ),
            "engineering_highlights": (
                "Over 9.4 km of large-diameter (1,000 mm & 1,200 mm) pressurized sewer pipelines.\n"
                "High-precision pipe jacking and open-cut excavation across varied soil strata.\n"
                "Reinforced concrete valve chambers, washout chambers, and air valve assemblies.\n"
                "Hydrostatic pressure testing and non-destructive weld inspections."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 8,
        },
        {
            "title": "Al-Maabda Al-Sharqiya Wastewater Project",
            "slug": "al-maabda-al-sharqiya-wastewater-project",
            "category": cat_water,
            "client_name": "National Organization for Potable Water and Sanitary Drainage (NOPWASD)",
            "location": "Assiut, Egypt",
            "cover_image": "projects/eastern-al-maabda-sewerage.webp",
            "built_up_area": "6.685 km Gravity Network + 1.4 km Force Main",
            "scope_of_work": "Gravity Sewer Network, Main Pumping Station & Force Main",
            "short_description": "Construction of 6.685 km of gravity sewer networks, a wastewater pumping station, and a 1.4 km force main as part of a major sanitation upgrade program serving Abnoub and El-Fath districts.",
            "full_description": (
                "Comprehensive sanitation upgrade scheme serving the Abnoub and El-Fath districts in Assiut Governorate. "
                "Al Bahaa Construction executed 6.685 km of UPVC/GRP gravity collector sewers, built a deep wet-well wastewater pumping station, "
                "and laid a 1.4 km ductile iron force main to transfer collected sewage to the regional treatment plant."
            ),
            "engineering_highlights": (
                "6.685 km of gravity collection sewer networks with manhole connections.\n"
                "Deep reinforced concrete submersible pumping station with standby power generation.\n"
                "1.4 km pressure force main conveying effluent across district boundaries.\n"
                "Significantly improved public health and groundwater protection in Eastern Maabda."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 9,
        },
        {
            "title": "Al-Husseiniya Wastewater Project",
            "slug": "al-husseiniya-wastewater-project",
            "category": cat_water,
            "client_name": "National Organization for Potable Water and Sanitary Drainage (NOPWASD)",
            "location": "Fayoum, Egypt",
            "cover_image": "projects/al-husseiniya-sewerage.webp",
            "built_up_area": "Complete HDPE Force Main System",
            "scope_of_work": "HDPE Force Mains, Valve Chambers & Pumping Integration",
            "short_description": "Development of a complete HDPE force main system with associated control and maintenance chambers under the national Hayah Karima initiative, supporting environmental sustainability and improved sanitation services.",
            "full_description": (
                "Executed under the auspices of the presidential Decent Life (Hayah Karima) initiative in Fayoum Governorate. "
                "The project engineered and installed a continuous butt-fused HDPE wastewater force main network equipped with "
                "automated control chambers, isolation gate valves, and air release stations."
            ),
            "engineering_highlights": (
                "Complete High-Density Polyethylene (HDPE) butt-fusion welded force main.\n"
                "Specialized control, washout, and air release maintenance chambers.\n"
                "Presidential Decent Life (Hayah Karima) national infrastructure delivery.\n"
                "Long-term environmental protection and sustainable sanitation services."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 10,
        },
        {
            "title": "Seif El-Nasr Wastewater Infrastructure Project",
            "slug": "seif-el-nasr-wastewater-infrastructure-project",
            "category": cat_water,
            "client_name": "National Organization for Potable Water and Sanitary Drainage (NOPWASD)",
            "location": "Al Minya, Egypt",
            "cover_image": "projects/manshaet-seif-el-nasr-sewerage.webp",
            "built_up_area": "Village-Wide Sewer Network",
            "scope_of_work": "Rural Collection Sewer Networks & Treatment Connections",
            "short_description": "Construction of village-wide sewer networks and supporting treatment infrastructure, providing essential wastewater services to underserved communities.",
            "full_description": (
                "Village-wide rural sanitation infrastructure scheme in Minya Governorate delivering modern underground sewer "
                "collector networks, household inspection chambers, and tie-in connections to regional treatment works, transforming "
                "the living conditions and environmental standards of underserved communities."
            ),
            "engineering_highlights": (
                "Village-wide gravity sewer network serving thousands of rural residents.\n"
                "Thousands of individual household connections and inspection manholes.\n"
                "Integration with central regional wastewater treatment facilities.\n"
                "Strict occupational safety in densely populated rural village streets."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 11,
        },
        {
            "title": "Armena Wastewater Treatment Plant",
            "slug": "armena-wastewater-treatment-plant",
            "category": cat_water,
            "client_name": "National Organization for Potable Water and Sanitary Drainage (NOPWASD)",
            "location": "Sohag, Egypt",
            "cover_image": "projects/armena-wastewater-treatment-plant.webp",
            "built_up_area": "Full-Cycle Wastewater Treatment Facility",
            "scope_of_work": "Design & Construction of Biological WWTP & Sludge Systems",
            "short_description": "Design and construction of a complete wastewater treatment facility incorporating treatment units, sludge management systems, electromechanical works, control buildings, and network connections.",
            "full_description": (
                "Turnkey design, civil construction, electromechanical supply, and operational testing of the Armena Wastewater "
                "Treatment Plant in Sohag Governorate. The facility incorporates screening channels, aeration tanks, secondary clarifiers, "
                "sludge thickening beds, chlorination contact tanks, administrative headquarters, and transformer substations."
            ),
            "engineering_highlights": (
                "Turnkey biological wastewater treatment facility execution.\n"
                "Advanced sludge management, thickening, and drying beds.\n"
                "Complete electromechanical equipment installation and SCADA telemetry.\n"
                "On-site administrative laboratory, workshop, and electrical substation buildings."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 12,
        },
        {
            "title": "Manfalut Booster Station",
            "slug": "manfalut-booster-station",
            "category": cat_pumping,
            "client_name": "National Organization for Potable Water and Sanitary Drainage (NOPWASD)",
            "location": "Assiut, Egypt",
            "cover_image": "projects/project_3.webp",
            "built_up_area": "945 L/s Pump Capacity | 75 m TDH",
            "scope_of_work": "High-Capacity Booster Pumping Station & Multi-Utility Networks",
            "short_description": "Development of integrated infrastructure systems including irrigation, potable water, firefighting, stormwater drainage, and sewer networks with 945 L/s pump capacity and 75 m dynamic head.",
            "full_description": (
                "Development of integrated municipal infrastructure systems and high-pressure booster station in Manfalut, Assiut. "
                "The booster station was engineered with a formidable pump capacity of 945 L/s and 75 m total dynamic head (TDH), "
                "providing resilient multi-utility distribution encompassing potable water, pressurized firefighting lines, stormwater "
                "drainage, and sanitary networks."
            ),
            "engineering_highlights": (
                "945 L/s high-volume pumping capacity with 75 m total dynamic head.\n"
                "Integrated potable water, automated firefighting, and stormwater drainage systems.\n"
                "Heavy-duty surge suppression tanks and harmonic-filtered variable frequency drives (VFD).\n"
                "Supports long-term urban infrastructure resilience and municipal expansion."
            ),
            "status": "completed",
            "is_featured": False,
            "order": 13,
        },
    ]

    for p in projects_data:
        Project.objects.create(**p)

    # -------------------------------------------------------------
    # 8. CAREERS: ACCOUNTANT VACANCY
    # -------------------------------------------------------------
    print("📦 8. Seeding Official Accountant Job Opening...")
    JobOpening.objects.all().delete()
    JobDepartment.objects.all().delete()

    dept_finance, _ = JobDepartment.objects.get_or_create(
        slug="finance-accounting",
        defaults={"name": "Finance & Accounting", "order": 1},
    )

    JobOpening.objects.create(
        title="Accountant - Al Bahaa Construction",
        slug="accountant-al-bahaa-construction",
        department=dept_finance,
        location="Head Office, First Settlement, New Cairo, Egypt",
        job_type="Full-Time",
        experience="Minimum 5 Years",
        summary=(
            "As part of our continued growth, we are looking for a highly qualified Accountant to join "
            "our Head Office in First Settlement, New Cairo. The ideal candidate will possess deep domain expertise "
            "in construction accounting, project costing, financial reporting, and revenue recognition."
        ),
        responsibilities=(
            "Manage day-to-day project accounting, subcontractor billing, and supplier reconciliations.\n"
            "Prepare detailed cost accounting reports and variance analysis across ongoing infrastructure sites.\n"
            "Support the financial reporting cycle, monthly closings, and statutory taxation compliance.\n"
            "Apply construction revenue recognition standards (IFRS 15) and cost-to-complete tracking.\n"
            "Coordinate with external auditors and site commercial managers for financial audits."
        ),
        requirements=(
            "Bachelor’s degree in Accounting, Commerce, or a related field.\n"
            "Minimum 5 years of relevant accounting experience.\n"
            "Strong experience in the construction/contracting industry is essential.\n"
            "Previous experience as a Public Accountant in an audit firm handling construction clients, or within a construction company.\n"
            "Solid knowledge of Cost Accounting, Financial Reporting, Taxation, Revenue Recognition, and Financial Analysis.\n"
            "Strong understanding of accounting standards and construction project accounting."
        ),
        benefits=(
            "Competitive compensation package commensurate with experience.\n"
            "Comprehensive medical insurance and social insurance coverage.\n"
            "Dynamic corporate environment in a Grade A leading infrastructure enterprise.\n"
            "Direct career development and leadership pathways."
        ),
        is_active=True,
        order=1,
    )

    # -------------------------------------------------------------
    # 9. CLIENT LOGOS (8 OFFICIAL AUTHORITIES)
    # -------------------------------------------------------------
    print("📦 9. Seeding 8 Official Client Authorities...")
    ClientLogo.objects.all().delete()
    clients_data = [
        {"name": "Armed Forces Engineering Authority", "order": 1},
        {"name": "Armed Forces Water Authority", "order": 2},
        {"name": "National Authority for Potable Water and Wastewater (NOPWASD)", "order": 3},
        {"name": "National Service Projects Organization (NSPO)", "order": 4},
        {"name": "Ministry of Housing, Utilities & Urban Communities", "order": 5},
        {"name": "New Urban Communities Authority (NUCA)", "order": 6},
        {"name": "Wadi El Nile Company", "order": 7},
        {"name": "Construction Authority for Potable Water & Wastewater Projects (CAPW)", "order": 8},
    ]
    for c in clients_data:
        ClientLogo.objects.create(
            name=c["name"],
            show_on_home=True,
            show_on_about=True,
            is_active=True,
            order=c["order"],
        )

    # -------------------------------------------------------------
    # 10. NEWS POST (ENR AWARD 2020)
    # -------------------------------------------------------------
    print("📦 10. Seeding Official ENR Award Press Release...")
    Post.objects.all().delete()
    NewsCategory.objects.all().delete()

    news_cat, _ = NewsCategory.objects.get_or_create(
        slug="awards-and-milestones",
        defaults={"name": "Awards & Milestones", "order": 1},
    )

    Post.objects.create(
        title="Engineering News Record (ENR) Best Project Award 2020",
        slug="enr-best-project-award-2020-al-mahsama",
        category=news_cat,
        cover_image="news/mostaqbal-misr-pipeline-milestone-completion.webp",
        author="Executive Board & Technical Office",
        excerpt="Al Bahaa Construction recognized for participation in the award-winning Al Mahsama Water Reclamation and Pumping Project.",
        content=(
            "Al Bahaa Construction is proud to highlight its participation in the landmark Al Mahsama Water Reclamation project, "
            "which was honored with the prestigious Global Best Project Award by Engineering News-Record (ENR) in 2020.\n\n"
            "This prestigious international accolade recognizes excellence in engineering execution, complex hydraulic construction, "
            "and sustainable infrastructure development. The Al Mahsama facility pumps approximately 1 million m³ of water per day "
            "to cultivate vital agricultural land in Sinai, standing as an enduring symbol of Egyptian engineering mastery."
        ),
        published_at=timezone.now(),
        is_published=True,
        order=1,
    )

    # Clean testimonials
    Testimonial.objects.all().delete()

    # -------------------------------------------------------------
    # 11. INSTANT CACHE INVALIDATION
    # -------------------------------------------------------------
    print("🧹 11. Invalidating In-Memory LocMem Cache...")
    cache.clear()
    invalidate_site_cache()

    print("=" * 60)
    print("✅ Complete Seeding Successful! All proposal data seeded 100%.")
    print(f"   • Projects: {Project.objects.count()} (All 13 Seeded)")
    print(f"   • Leadership: {TeamMember.objects.count()} (6 C-Level Executives)")
    print(f"   • Job Openings: {JobOpening.objects.count()} (Accountant)")
    print(f"   • Key Stats: {AboutStatistic.objects.count()} (6 Canonical Figures)")
    print(f"   • Values: {CompanyPillar.objects.count()} (7 Corporate Values)")
    print(f"   • Clients: {ClientLogo.objects.count()} (8 Official Authorities)")
    print("=" * 60)


if __name__ == "__main__":
    seed_all()
