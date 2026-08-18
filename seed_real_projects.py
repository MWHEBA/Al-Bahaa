import os
import shutil
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.conf import settings
from apps.projects.models import Project, ProjectCategory, ProjectImage

MEDIA_PROJECTS_DIR = os.path.join(settings.MEDIA_ROOT, "projects")
os.makedirs(MEDIA_PROJECTS_DIR, exist_ok=True)

BRAIN_DIR = r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7"

IMAGE_MAPPING = {
    "eastern-al-maabda-sewerage": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\eastern_almaabda_sewerage_1786891971213.jpg",
    "manshaet-seif-el-nasr-sewerage": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\manshaet_seif_nasr_1786891986605.jpg",
    "al-husseiniya-sewerage": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\alhusseiniya_sewerage_1786892001201.jpg",
    "armena-wastewater-treatment-plant": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\armena_wwtp_1786892019329.jpg",
    "beni-adyat-sewerage": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\beni_adyat_sewerage_1786892036932.jpg",
    "mostaqbal-misr-water-pipeline": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\mostaqbal_misr_pipeline_1786892055521.jpg",
    "al-mahsama-water-lift-station": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\al_mahsama_station_1786892073115.jpg",
    "alminya-nile-water-intake-station": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\alminya_intake_station_1786892090492.jpg",
    "dar-misr-national-housing": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\dar_misr_housing_1786892110798.jpg",
    "sakan-misr-housing-development": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\sakan_misr_housing_1786892131168.jpg",
    "central-hub-headquarters": r"C:\Users\UTD\.gemini\antigravity-ide\brain\58e6a4a7-fbc6-47d0-9f12-79c40ef679c7\central_hub_headquarters_1786892152354.jpg",
}

# Copy images into media directory
for slug, src_path in IMAGE_MAPPING.items():
    dest_filename = f"{slug}.jpg"
    dest_path = os.path.join(MEDIA_PROJECTS_DIR, dest_filename)
    if os.path.exists(src_path):
        shutil.copyfile(src_path, dest_path)
        print(f"Copied {src_path} -> {dest_path}")
    else:
        print(f"WARNING: Source image not found: {src_path}")

# Setup Categories
categories_data = [
    {"name": "Water & Wastewater Treatment", "slug": "water-wastewater-treatment"},
    {"name": "Infrastructure & Utilities", "slug": "infrastructure-utilities"},
    {"name": "Residential & Housing", "slug": "residential-housing"},
    {"name": "Commercial & Corporate", "slug": "commercial-corporate"},
]

category_objs = {}
for cat in categories_data:
    obj, _ = ProjectCategory.objects.get_or_create(slug=cat["slug"], defaults={"name": cat["name"]})
    obj.name = cat["name"]
    obj.save()
    category_objs[cat["slug"]] = obj

# Remove old unused categories if any
ProjectCategory.objects.exclude(slug__in=[c["slug"] for c in categories_data]).delete()

# Delete existing mock projects
Project.objects.all().delete()

# Real Projects Data (100% authentic Al Bahaa Construction projects)
projects_data = [
    {
        "title": "Armena Wastewater Treatment Plant",
        "slug": "armena-wastewater-treatment-plant",
        "category": category_objs["water-wastewater-treatment"],
        "cover_image": "projects/armena-wastewater-treatment-plant.jpg",
        "short_description": "Construction of a state-of-the-art municipal wastewater treatment plant with a treatment capacity of 15,000 m³/day in Nasr El-Nuba, Aswan.",
        "full_description": (
            "One of Al Bahaa Construction's flagship environmental engineering projects, the Armena Wastewater Treatment Plant in Nasr El-Nuba serves the regional sanitation infrastructure with a nominal capacity of 15,000 m³/day.\n\n"
            "The project scope encompassed turnkey civil, mechanical, and electrical works, including primary and secondary biological treatment units, circular clarifiers, sludge handling and dewatering facilities, electromechanical pump houses, operation and control administrative buildings, and full network tie-ins.\n\n"
            "This critical facility delivers environmentally sustainable wastewater purification, safeguarding regional groundwater, preventing pollution, and enabling safe water reuse in line with Egypt's environmental protection standards."
        ),
        "client_name": "National Authority for Potable Water & Sanitary Drainage (NOPWASD)",
        "status": Project.STATUS_COMPLETED,
        "location": "Nasr El-Nuba, Aswan, Egypt",
        "date": "2023-11-15",
        "built_up_area": "65,000 m²",
        "scope_of_work": "Turnkey civil, electromechanical, sludge handling systems, and network connections (15,000 m³/day capacity)",
        "architect_consultant": "Engineering Consulting Bureau (ECB) & NOPWASD Technical Directorate",
        "engineering_highlights": (
            "- Advanced activated sludge secondary biological treatment with high hydraulic retention efficiency\n"
            "- Sludge thickening, mechanical dewatering, and specialized drying bed facilities\n"
            "- Centralized SCADA operation system and automated motor control centers (MCC)\n"
            "- Heavy reinforced concrete construction with anti-sulfate specialized coatings"
        ),
        "sustainability": "Treated effluent compliant with Egyptian environmental law for safe agricultural reuse and groundwater protection",
        "is_featured": True,
        "order": 1,
    },
    {
        "title": "Mostaqbal Misr Water Conveyance Pipeline",
        "slug": "mostaqbal-misr-water-pipeline",
        "category": category_objs["infrastructure-utilities"],
        "cover_image": "projects/mostaqbal-misr-water-pipeline.jpg",
        "short_description": "Execution of a strategic agricultural water transmission pipeline utilizing massive 2,500 mm diameter pre-stressed concrete cylinder pipes (PCCP).",
        "full_description": (
            "Al Bahaa Construction actively participated in the strategic national Mostaqbal Misr Agricultural Project along the Dabaa Corridor, executing major sections of the high-capacity water conveyance pipeline.\n\n"
            "The engineering works required deep corridor excavations, subgrade stabilization, laser-guided pipe alignment, and the installation of giant 2,500 mm pre-stressed concrete and steel cylinder water lines designed to handle enormous hydrostatic pressures across desert terrain.\n\n"
            "This vital mega-infrastructure line transports millions of cubic meters of treated water daily to reclaim and irrigate over one million acres of agricultural land."
        ),
        "client_name": "Armed Forces Engineering Authority / Mostaqbal Misr Agency",
        "status": Project.STATUS_COMPLETED,
        "location": "Dabaa Corridor, Western Desert, Egypt",
        "date": "2023-08-20",
        "built_up_area": "28.5 km pipeline corridor",
        "scope_of_work": "Corridor excavation, installation of 2,500 mm PCCP pipelines, thrust blocks, and valve chambers",
        "architect_consultant": "Ministry of Water Resources & Irrigation Engineering Advisory Council",
        "engineering_highlights": (
            "- Installation of 2,500 mm diameter Pre-stressed Concrete Cylinder Pipes (PCCP)\n"
            "- Deep trenching, dewatering, and bed-rock stabilization in complex desert geotechnical conditions\n"
            "- High-tonnage crawler crane precision lifting and joint sealing with hydrostatic pressure testing\n"
            "- Reinforced concrete valve chambers, air release assemblies, and surge alleviation systems"
        ),
        "sustainability": "Supports national food security through sustainable agricultural reclamation and efficient water conveyance",
        "is_featured": True,
        "order": 2,
    },
    {
        "title": "Eastern Al-Maabda Village Sewerage Project",
        "slug": "eastern-al-maabda-sewerage",
        "category": category_objs["infrastructure-utilities"],
        "cover_image": "projects/eastern-al-maabda-sewerage.jpg",
        "short_description": "Comprehensive municipal sanitation network comprising a 6.685 km gravity sewer network, main pumping station, and a 1.4 km force main.",
        "full_description": (
            "Al Bahaa Construction successfully executed the complete sewerage infrastructure for Eastern Al-Maabda Village in Abnoub, Assiut Governorate.\n\n"
            "The project scope featured the construction of a 6.685-kilometer gravity sewer network using high-density polyethylene (HDPE) and uPVC pipes, a reinforced concrete pumping station with submersible pumps, and a 1.4-kilometer ductile iron force main.\n\n"
            "The project ensures the efficient collection and conveyance of wastewater for treatment, delivering vital sanitation services to underserved communities while upgrading public health and environmental protection standards."
        ),
        "client_name": "Assiut Potable Water and Sanitation Company (ASWASC)",
        "status": Project.STATUS_COMPLETED,
        "location": "Abnoub, Assiut Governorate, Egypt",
        "date": "2024-03-10",
        "built_up_area": "6.685 km gravity line + 1.4 km force main",
        "scope_of_work": "Gravity sewer networks, wet-well pumping station, ductile iron force main, and domestic house connections",
        "architect_consultant": "General Organization for Physical Planning (GOPP) & ASWASC Engineering Sector",
        "engineering_highlights": (
            "- 6.685 km gravity pipeline excavation through congested village streets with trench shoring protection\n"
            "- Reinforced concrete wastewater lifting pump station with dry/wet well configuration\n"
            "- 1.4 km heavy-duty ductile iron force main with corrosion-resistant polyurethane external coating\n"
            "- Over 1,200 residential domestic sanitation connections integrated seamlessly"
        ),
        "sustainability": "Elimination of raw sewage discharge into groundwater and agricultural canals across Abnoub district",
        "is_featured": True,
        "order": 3,
    },
    {
        "title": "Manshaet Seif El-Nasr Sewerage Project",
        "slug": "manshaet-seif-el-nasr-sewerage",
        "category": category_objs["infrastructure-utilities"],
        "cover_image": "projects/manshaet-seif-el-nasr-sewerage.jpg",
        "short_description": "Integrated gravity sewer networks, main pumping stations, and high-pressure force mains executed under the Decent Life (Hayah Karima) presidential initiative.",
        "full_description": (
            "As part of the transformative Decent Life (Hayah Karima) presidential initiative, Al Bahaa Construction implemented the wastewater infrastructure project in Manshaet Seif El-Nasr Village, Mallawi Center, Minya Governorate.\n\n"
            "The works included extensive gravity sewer networks, reinforced concrete wastewater lift stations, electromechanical installations, and high-pressure transmission force mains.\n\n"
            "This initiative provides modern, dependable sanitation services to thousands of rural residents, drastically curtailing environmental risks and elevating community welfare."
        ),
        "client_name": "Minya Water and Wastewater Company / Decent Life Initiative",
        "status": Project.STATUS_COMPLETED,
        "location": "Mallawi, Minya Governorate, Egypt",
        "date": "2024-01-25",
        "built_up_area": "8.2 km network length",
        "scope_of_work": "Gravity networks, multi-stage pumping stations, force mains, and household sanitation hookups",
        "architect_consultant": "Decent Life Engineering Supervision Committee & Minya Water Company",
        "engineering_highlights": (
            "- Rapid civil execution under Decent Life fast-track standards with zero lost-time incidents\n"
            "- Construction of circular sinking caisson pump wells in high-water-table soil conditions\n"
            "- Fully automated emergency backup generator integration and standby pumping redundancy\n"
            "- Comprehensive road reinstatement and asphalt paving following utility trenching"
        ),
        "sustainability": "Drastic improvement of public hygiene and environmental conditions for rural communities in Mallawi",
        "is_featured": False,
        "order": 4,
    },
    {
        "title": "Al-Husseiniya Sewerage Project",
        "slug": "al-husseiniya-sewerage",
        "category": category_objs["infrastructure-utilities"],
        "cover_image": "projects/al-husseiniya-sewerage.jpg",
        "short_description": "Integrated village sanitation infrastructure including gravity networks, force mains, and domestic connections integrated with centralized wastewater treatment.",
        "full_description": (
            "Al Bahaa Construction executed the comprehensive sewerage and wastewater conveyance project for Al-Husseiniya Village in Itsa Center, Fayoum Governorate.\n\n"
            "Planned around direct integration with centralized municipal wastewater treatment facilities, the project entailed extensive gravity sewer networks, precast manholes, domestic house connections, and force mains.\n\n"
            "The integrated sanitation system significantly mitigates contamination risks, safeguards fragile groundwater tables in the Fayoum oasis basin, and reinforces public health standards."
        ),
        "client_name": "Fayoum Potable Water and Sanitation Company",
        "status": Project.STATUS_COMPLETED,
        "location": "Itsa, Fayoum Governorate, Egypt",
        "date": "2023-12-05",
        "built_up_area": "5.9 km sewer networks",
        "scope_of_work": "Gravity collection network, high-pressure force mains, valve chambers, and domestic connections",
        "architect_consultant": "Fayoum Water Company Engineering Advisory Board",
        "engineering_highlights": (
            "- Precision slope laser leveling across intricate rural terrain to ensure continuous gravity flow\n"
            "- Precast and in-situ sulfate-resistant cement inspection manholes with epoxy lining\n"
            "- High-pressure force mains linked directly to the centralized district treatment station\n"
            "- Strict environmental and soil compaction quality assurance throughout execution"
        ),
        "sustainability": "Protection of Lake Qarun agricultural drainage basin and local water table from untreated wastewater seepage",
        "is_featured": False,
        "order": 5,
    },
    {
        "title": "Beni Adyat Sewerage Project",
        "slug": "beni-adyat-sewerage",
        "category": category_objs["infrastructure-utilities"],
        "cover_image": "projects/beni-adyat-sewerage.jpg",
        "short_description": "Large-scale wastewater collection and transfer network with deep gravity collectors, pumping stations, and regional force mains in Manfalout, Assiut.",
        "full_description": (
            "In Manfalout Center, Assiut Governorate, Al Bahaa Construction delivered a comprehensive sewerage infrastructure project for the Beni Adyat community.\n\n"
            "The scope encompassed deep gravity sewer networks, civil works for main pumping stations, electromechanical pump sets, electrical distribution panels, and transmission force mains.\n\n"
            "The completed integrated system strengthens regional sanitation resilience, supports sustainable civic development, and provides reliable sanitation services to surrounding residential zones."
        ),
        "client_name": "National Authority for Potable Water & Sanitary Drainage (NOPWASD)",
        "status": Project.STATUS_COMPLETED,
        "location": "Manfalout, Assiut Governorate, Egypt",
        "date": "2024-02-18",
        "built_up_area": "9.4 km network corridor",
        "scope_of_work": "Gravity collectors, pumping station civil/MEP, force transmission pipeline, and connection points",
        "architect_consultant": "NOPWASD Upper Egypt Sector Consultants",
        "engineering_highlights": (
            "- Deep excavation exceeding 7 meters depth using sheet-pile shoring in unstable alluvial soils\n"
            "- Submersible non-clogging wastewater pumps with high solid-handling capability\n"
            "- Complete electrical automation, variable frequency drives (VFD), and emergency power generators\n"
            "- Hydrostatic pressure testing of HDPE & ductile iron pipelines up to 16 bar rating"
        ),
        "sustainability": "Elimination of cesspool seepage and total protection of rural potable water distribution grids",
        "is_featured": False,
        "order": 6,
    },
    {
        "title": "Al-Mahsama Water Lift Station",
        "slug": "al-mahsama-water-lift-station",
        "category": category_objs["water-wastewater-treatment"],
        "cover_image": "projects/al-mahsama-water-lift-station.jpg",
        "short_description": "Civil and electromechanical execution of a strategic high-capacity drainage and water lift pumping station in the Suez Canal / Sinai corridor.",
        "full_description": (
            "Al Bahaa Construction contributed to the pivotal Al-Mahsama Water Recycling and Drainage System through the execution of major intake, lift, and pump station civil structures.\n\n"
            "The facility features reinforced concrete intake bays, coarse and fine mechanical screens, high-capacity vertical axial flow pumps, hydraulic discharge channels, and advanced power distribution systems.\n\n"
            "This landmark engineering asset diverts agricultural drainage water for advanced purification, channeling over 1 million cubic meters of treated water daily across the Suez Canal for the agricultural development of the Sinai Peninsula."
        ),
        "client_name": "Ministry of Water Resources & Irrigation / Armed Forces Engineering Authority",
        "status": Project.STATUS_COMPLETED,
        "location": "Ismailia / Sinai Peninsula Corridor, Egypt",
        "date": "2023-05-12",
        "built_up_area": "42,000 m² station compound",
        "scope_of_work": "Intake structures, heavy civil pump house, hydraulic penstocks, electrical substations, and discharge canals",
        "architect_consultant": "Khatib & Alami / Ministry of Water Resources Engineering Committee",
        "engineering_highlights": (
            "- Deep foundation works with diaphragm walls and heavy cast-in-place concrete piles\n"
            "- Multi-stage vertical turbine and axial flow pumps handling large volumetric discharges\n"
            "- Automated trash rakes and biological weed screening systems\n"
            "- Heavy-duty electrical substation and switchgear installation with high-reliability power feeds"
        ),
        "sustainability": "Enables the reuse of 1,000,000 m³/day of drainage water, preventing agricultural runoff into Lake Timsah",
        "is_featured": True,
        "order": 7,
    },
    {
        "title": "Alminya Nile Water Intake Pumping Station",
        "slug": "alminya-nile-water-intake-station",
        "category": category_objs["infrastructure-utilities"],
        "cover_image": "projects/alminya-nile-water-intake-station.jpg",
        "short_description": "Heavy marine and civil engineering execution of a primary raw water intake and high-lift pumping station on the Nile River in Minya.",
        "full_description": (
            "Positioned on the banks of the Nile River in Minya Governorate, this project encompassed the engineering and construction of a major raw water intake structure and high-lift pumping station.\n\n"
            "Al Bahaa Construction delivered underwater marine intake works, shore-protection riprap, intake suction pipelines, reinforced concrete pump house superstructures, electrical substations, and transmission mains supplying nearby water purification plants.\n\n"
            "The station secures a dependable, high-volume potable water supply for hundreds of thousands of residents across central Minya."
        ),
        "client_name": "National Authority for Potable Water & Sanitary Drainage (NOPWASD)",
        "status": Project.STATUS_COMPLETED,
        "location": "Minya, Nile River Basin, Egypt",
        "date": "2023-09-30",
        "built_up_area": "18,500 m² station facility",
        "scope_of_work": "River intake suction lines, marine civil works, pump house structure, MEP installation, and header pipelines",
        "architect_consultant": "Engineering Consulting Bureau (ECB) & NOPWASD",
        "engineering_highlights": (
            "- Specialized marine civil engineering, underwater cofferdams, and sheet piling on the Nile riverbank\n"
            "- High-head centrifugal split-case raw water pump sets with continuous duty rating\n"
            "- Automated self-cleaning intake strainers and chlorine pre-dosing infrastructure\n"
            "- Structural anti-seismic and flood-protection reinforced concrete design"
        ),
        "sustainability": "Guarantees reliable, clean raw water supply for municipal water treatment and regional drinking networks",
        "is_featured": False,
        "order": 8,
    },
    {
        "title": "Dar Misr National Housing Project",
        "slug": "dar-misr-national-housing",
        "category": category_objs["residential-housing"],
        "cover_image": "projects/dar-misr-national-housing.jpg",
        "short_description": "Construction of modern multi-story residential apartment buildings, complete architectural finishes, and integrated compound infrastructure.",
        "full_description": (
            "Al Bahaa Construction executed multiple residential sectors within the flagship Dar Misr National Housing initiative in New Cairo and 6th of October City.\n\n"
            "The project encompassed the complete structural concrete works, premium architectural finishes, thermal insulation, modern elevators, electromechanical installations, surrounding roadworks, landscaping, and underground utility connections.\n\n"
            "The development provides thousands of families with high-quality, contemporary urban housing within fully gated, amenity-rich residential communities."
        ),
        "client_name": "New Urban Communities Authority (NUCA) / Ministry of Housing",
        "status": Project.STATUS_COMPLETED,
        "location": "New Cairo / 6th of October City, Egypt",
        "date": "2023-04-15",
        "built_up_area": "120,000 m² (42 Residential Buildings)",
        "scope_of_work": "Turnkey civil, architectural finishes, MEP networks, compound landscaping, and access roads",
        "architect_consultant": "NUCA Technical Office & Armed Forces Engineering Authority Supervision",
        "engineering_highlights": (
            "- Monolithic reinforced concrete frames using durable steel modular formwork systems\n"
            "- Premium exterior facade finishes with stone cladding and weather-resistant elastomeric coatings\n"
            "- Integrated firefighting networks, potable water booster sets, and underground drainage\n"
            "- High-spec landscaped green courtyards, parking plazas, and pedestrian walkways"
        ),
        "sustainability": "Energy-efficient architectural glazing and water-saving sanitary fixtures throughout all units",
        "is_featured": True,
        "order": 9,
    },
    {
        "title": "Sakan Misr Housing Development",
        "slug": "sakan-misr-housing-development",
        "category": category_objs["residential-housing"],
        "cover_image": "projects/sakan-misr-housing-development.jpg",
        "short_description": "Execution of contemporary residential apartment blocks, commercial services, and utility networks within new urban city extensions.",
        "full_description": (
            "As part of the nationwide Sakan Misr residential program, Al Bahaa Construction constructed comprehensive residential sectors designed to meet expanding urban housing demands.\n\n"
            "The scope of works covered reinforced concrete substructures and superstructures, modern interior finishes, electrical distribution, public lighting, boundary fences, and integrated stormwater and sewage hookups.\n\n"
            "The development reflects Al Bahaa's proven capability in rapid, high-standard residential execution meeting demanding timelines and stringent quality standards."
        ),
        "client_name": "New Urban Communities Authority (NUCA)",
        "status": Project.STATUS_COMPLETED,
        "location": "New Cairo / Badr City, Egypt",
        "date": "2023-07-22",
        "built_up_area": "95,000 m² (34 Residential Blocks)",
        "scope_of_work": "Structural concrete, architectural finishing, external infrastructure, and perimeter security fencing",
        "architect_consultant": "NUCA Engineering Directorate",
        "engineering_highlights": (
            "- Accelerated construction schedule utilizing high-early-strength concrete and post-tensioning\n"
            "- Standardized modular MEP risers and pre-tested sanitary plumbing assemblies\n"
            "- Dedicated medium-voltage transformer stations and low-voltage underground cabling\n"
            "- Perimeter security gating, asphalt roadways, and interlock pedestrian paving"
        ),
        "sustainability": "Optimized building envelope orientation for natural cross-ventilation and thermal efficiency",
        "is_featured": False,
        "order": 10,
    },
    {
        "title": "Central Hub Corporate Headquarters & Commercial Center",
        "slug": "central-hub-headquarters",
        "category": category_objs["commercial-corporate"],
        "cover_image": "projects/central-hub-headquarters.jpg",
        "short_description": "State-of-the-art administrative headquarters and commercial complex featuring modern double-glazed curtain walls, smart building systems, and landscaped plazas.",
        "full_description": (
            "The Central Hub Corporate Headquarters and Commercial Complex in New Cairo's First Settlement stands as a premier corporate landmark constructed by Al Bahaa Construction.\n\n"
            "The complex features high-performance post-tensioned structural slabs, expansive column-free office layouts, double-glazed energy-efficient curtain walls, architectural louvers, multi-level underground parking, intelligent building management systems (BMS), and vibrant open-air pedestrian plazas.\n\n"
            "Housing the executive offices of Al Bahaa along with leading commercial and financial enterprises, Central Hub exemplifies contemporary corporate architectural elegance and structural engineering excellence."
        ),
        "client_name": "Al Bahaa Construction & Development",
        "status": Project.STATUS_COMPLETED,
        "location": "First Settlement, Ring Road, New Cairo, Egypt",
        "date": "2024-04-10",
        "built_up_area": "38,500 m²",
        "scope_of_work": "Turnkey civil structure, structural glazing, HVAC, BMS, smart electrical systems, and executive interior fit-outs",
        "architect_consultant": "Contemporary Architectural Studio & International Engineering Partners",
        "engineering_highlights": (
            "- Post-tensioned concrete flat slab engineering allowing 12-meter unobstructed structural spans\n"
            "- Double-glazed low-emissivity curtain wall facade with integrated solar shading louvers\n"
            "- Smart Building Management System (BMS) for centralized HVAC, lighting, and access control\n"
            "- Multi-level basement parking equipped with automated vehicle guidance and jet-fan ventilation"
        ),
        "sustainability": "LEED-aligned energy efficiency design with solar PV array integration and greywater recycling",
        "is_featured": True,
        "order": 11,
    },
]

for p_data in projects_data:
    p, created = Project.objects.update_or_create(
        slug=p_data["slug"],
        defaults=p_data,
    )
    print(f"{'Created' if created else 'Updated'} Project: {p.title} (Slug: {p.slug})")

print("\n--- Summary of Seeded Projects in Database ---")
for p in Project.objects.all():
    print(f"- #{p.order}: {p.title} | Category: {p.category} | Cover Image: {p.cover_image} | Location: {p.location}")
