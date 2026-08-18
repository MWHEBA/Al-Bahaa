import os
import shutil
from pathlib import Path
from django.conf import settings
from django.core.cache import cache
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apps.core.models import (
    AboutContent,
    AboutStatistic,
    CareerPillar,
    CareerSettings,
    ClientLogo,
    CompanyPillar,
    ContactMessage,
    HomeContent,
    JobApplication,
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


class Command(BaseCommand):
    help = "Hydrates 100% of Al Bahaa CMS content and copies media files from static to media storage."

    def copy_media_file(self, static_rel_path, media_subfolder, target_filename):
        """Helper to copy a file from static/ to media/ and return a Django File object."""
        static_file = settings.BASE_DIR / "static" / static_rel_path
        if not static_file.exists():
            self.stdout.write(self.style.WARNING(f"Static file missing: {static_file}"))
            return None

        media_dir = settings.MEDIA_ROOT / media_subfolder
        media_dir.mkdir(parents=True, exist_ok=True)

        target_file = media_dir / target_filename
        shutil.copy2(static_file, target_file)

        return File(open(target_file, "rb"), name=f"{media_subfolder}/{target_filename}")

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(">>> Starting 100% CMS Data & Media Hydration..."))

        # 1. Site Settings
        self.stdout.write("  [1/9] Hydrating Site Settings & Branding...")
        settings_obj = SiteSettings.load()
        settings_obj.company_name = "Al Bahaa Contracting (S.A.E)"
        settings_obj.phone_main = "+20 (2) 2389 9255"
        settings_obj.phone_tenders = "+20 (10) 0123 4567"
        settings_obj.phone_sale = "+20 (2) 2389 9255"
        settings_obj.phone_support = "+20 (10) 0123 4567"
        settings_obj.email_general = "info@albahaacontracting.com"
        settings_obj.email_tenders = "tenders@albahaacontracting.com"
        settings_obj.email_careers = "careers@albahaacontracting.com"
        settings_obj.address = "Central Hub, Units 213-217, First Settlement, New Cairo, Egypt"
        settings_obj.address_line1 = "Central Hub, Units 213-217"
        settings_obj.address_line2 = "First Settlement, New Cairo, Egypt"
        settings_obj.map_embed_url = "https://maps.google.com/maps?q=30.0633628,31.4215952+(Al+Bahaa+Contracting+-+Central+Hub)&t=&z=16&ie=UTF8&iwloc=&output=embed"
        settings_obj.map_directions_url = "https://maps.app.goo.gl/wxBbUA5jU5uGwDTZ7"
        settings_obj.working_hours_weekdays = "Sunday – Thursday: 8:00 AM – 5:00 PM"
        settings_obj.working_hours_emergencies = "Friday & Saturday: Site Emergencies Only"
        settings_obj.linkedin_url = "https://linkedin.com"
        settings_obj.facebook_url = "https://facebook.com"
        settings_obj.instagram_url = "https://instagram.com"
        settings_obj.youtube_url = "https://youtube.com"
        settings_obj.footer_quote = "Established in 1986, AlBahaa delivers integrated contracting, finishing, and construction solutions across Egypt."
        settings_obj.footer_quote_author = "Al Bahaa Contracting"
        settings_obj.copyright_text = "© 2026 ALBAHAA CONSTRUCTION. ALL RIGHTS RESERVED"

        f_header = self.copy_media_file("img/branding/AlBahaa logo.svg", "branding", "header_logo.svg")
        if f_header:
            settings_obj.header_logo.save("header_logo.svg", f_header, save=False)

        f_footer = self.copy_media_file("img/branding/AlBahaa logo - square.svg", "branding", "footer_logo.svg")
        if f_footer:
            settings_obj.footer_logo.save("footer_logo.svg", f_footer, save=False)

        f_fav = self.copy_media_file("img/branding/AlBahaa logo.svg", "branding", "favicon.svg")
        if f_fav:
            settings_obj.favicon.save("favicon.svg", f_fav, save=False)

        settings_obj.save()

        # 2. Page Heroes
        self.stdout.write("  [2/9] Hydrating Page Hero Banners...")
        heroes_data = [
            ("home", "AL BAHAA CONTRACTING (S.A.E)", "ENGINEERING EXCELLENCE &", "CIVIL INFRASTRUCTURE", "Established in 1986, Al Bahaa delivers Grade A water networks, turnkey civil construction, and enduring architectural landmarks across Egypt with disciplined execution.", "img/home/Rectangle 3.png", "home_hero.png"),
            ("about", "About Al Bahaa", "We like to build", "things people use.", "An Egyptian joint stock company with more than 30 years of engineering leadership, Grade A infrastructure classification, and turnkey project delivery.", "img/about/Rectangle 21.png", "about_hero.png"),
            ("projects", "Featured Projects", "Built work", "with lasting value.", "A focused collection of civil, administrative, and commercial infrastructure shaped with precision and engineered for long-term use.", "img/projects/projects-hero-banner.jpg", "projects_hero.jpg"),
            ("news", "NEWS & INSIGHTS", "Updated news.", "", "Engineering milestones, technical insights, and corporate updates across landmark infrastructure projects in Egypt.", "img/news/news-hero-banner.jpg", "news_hero.jpg"),
            ("careers", "Careers at Al Bahaa", "Build enduring landmarks", "with our team.", "Join a disciplined, high-caliber engineering force shaping Egypt's major infrastructure, municipal networks, and commercial landmarks.", "img/careers/careers-hero-banner.jpg", "careers_hero.jpg"),
            ("contact", "Contact Al Bahaa", "Start a conversation", "about your next project.", "Direct channels for tenders, subcontractor registrations, procurement inquiries, and engineering consultations with our leadership.", "img/contact/contact-hero-recovered.png", "contact_hero.png"),
        ]
        for page_code, eyebrow, t1, t2, desc, img_path, out_name in heroes_data:
            hero, _ = PageHero.objects.get_or_create(page=page_code)
            hero.eyebrow = eyebrow
            hero.title_line1 = t1
            hero.title_line2 = t2
            hero.description = desc
            f_hero = self.copy_media_file(img_path, "heroes", out_name)
            if f_hero:
                hero.hero_image.save(out_name, f_hero, save=False)
            hero.save()

        # 3. Home Content & Specializations
        self.stdout.write("  [3/9] Hydrating Home Content & Specializations...")
        home_content = HomeContent.load()
        home_content.blueprints_eyebrow = "OUR SPECIALIZATION"
        home_content.blueprints_title_line1 = "WE TURN BLUEPRINTS INTO"
        home_content.blueprints_title_line2 = "ENDURING REALITY."
        home_content.blueprints_description = "With more than three decades of engineering leadership and active membership in the Egyptian Federation for Construction, Al Bahaa delivers turnkey civil, residential, and infrastructure landmarks on schedule, within budget, and to the highest QA/QC standards."
        home_content.blueprints_btn_text = "View More"
        home_content.blueprints_btn_url = "/about/"
        f_blueprints = self.copy_media_file("img/home/Rectangle 8.png", "home", "blueprints_image.png")
        if f_blueprints:
            home_content.blueprints_image.save("blueprints_image.png", f_blueprints, save=False)
        home_content.save()

        specs_data = [
            ("GRADE A INFRASTRUCTURE", "Municipal Water Transmission & Collector Networks", "Specialized in municipal water transmission pipelines, sewage collector networks, pumping stations, and stormwater drainage systems engineered to exacting standards.", 1),
            ("CIVIL & STRUCTURAL WORKS", "Heavy Reinforced Concrete & Deep Foundations", "Heavy reinforced concrete structures, deep foundation earthworks, structural steel framing, and institutional facilities built for enduring durability.", 2),
            ("TURNKEY GENERAL CONTRACTING", "Commercial & Residential Landmarks", "Comprehensive end-to-end project execution from initial site earthworks and BIM coordination to high-end architectural finishes delivered on schedule.", 3),
            ("ELECTROMECHANICAL & MEP", "Integrated MEP, BMS & Substation Engineering", "Advanced electro-mechanical installations, automated pump station control, value engineering, and high-efficiency MEP infrastructure.", 4),
        ]
        SpecializationItem.objects.all().delete()
        for disc, title, desc, ord_num in specs_data:
            SpecializationItem.objects.create(discipline=disc, title=title, description=desc, order=ord_num, is_active=True)

        # 4. About Content, Stats, Pillars, Services, Team
        self.stdout.write("  [4/9] Hydrating About Content, Credentials, Pillars & Leadership...")
        about_content = AboutContent.load()
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

        stats_data = [
            ("30+", "Years of Industry Experience (Est. 1986)", 1),
            ("Grade A", "Water & Sewage Infrastructure Classification", 2),
            ("1994", "Active Member, Egyptian Federation of Contractors", 3),
            ("S.A.E", "Egyptian Joint Stock Enterprise (Inc. 2000)", 4),
        ]
        AboutStatistic.objects.all().delete()
        for val, lbl, o in stats_data:
            AboutStatistic.objects.create(value=val, label=lbl, order=o, is_active=True)

        pillars_data = [
            ("01", "Technical Rigor & QA/QC", "Leveraging state-of-the-art BIM modeling, advanced construction methods, and comprehensive QA/QC processes for flawless structural integrity.", 1),
            ("02", "Safety & Zero-Harm Protocol", "Enforcing uncompromising occupational health and safety protocols across all active job sites, safeguarding our workforce and communities.", 2),
            ("03", "Sustainable Value Delivery", "Integrating resource-efficient materials, lifecycle value engineering, and resilient construction practices built to endure for generations.", 3),
        ]
        CompanyPillar.objects.all().delete()
        for num, title, desc, o in pillars_data:
            CompanyPillar.objects.create(number=num, title=title, description=desc, order=o, is_active=True)

        services_data = [
            ("Water & Sewage Infrastructure (Grade A)", "Extensive municipal water transmission mains, sewage collector networks, pumping stations, and stormwater drainage systems engineered to exacting standards.", 1),
            ("Residential & Commercial Developments", "Integrated residential communities, commercial hubs, and institutional headquarters delivered with disciplined execution and refined architectural finishes.", 2),
            ("Turnkey Civil & General Contracting", "Heavy civil works, deep foundation earthworks, structural concrete, and logistical infrastructure built for enduring durability.", 3),
            ("Specialized MEP & Value Engineering", "Advanced electro-mechanical installations, BIM coordination, stringent QA/QC protocols, and lifecycle cost optimization.", 4),
        ]
        ServiceItem.objects.all().delete()
        for title, desc, o in services_data:
            ServiceItem.objects.create(title=title, description=desc, order=o, is_active=True)

        # Team
        TeamMember.objects.all().delete()
        # Founder
        TeamMember.objects.create(
            name="Eng. Mohamed Bahaa El Din Abdalla",
            position="Founder & Chairman",
            member_type="founder",
            quote="Engineering leadership rooted in precision, integrity, and enduring value.",
            bio="Beginning his career at Arab Contractors until 1978, he subsequently led regional operations as Regional Director in Medina at Aziz Company for Contracting and Industrial Investment. In 1986, he co-founded Albahaa Contracting, dedicating full executive leadership to establishing the company as one of Egypt's premier Grade A engineering and infrastructure enterprises.",
            order=1,
            is_active=True,
        )
        # CEO
        ceo = TeamMember.objects.create(
            name="Eng. Ahmed Bahaa",
            position="CEO / Board Member",
            member_type="executive",
            quote="Executing infrastructure with uncompromising technical rigor, punctuality, and fiscal responsibility.",
            bio="Directing group operations and strategic project delivery across Egypt.",
            order=2,
            is_active=True,
        )
        f_ceo = self.copy_media_file("img/team/ahmed-bahaa.jpg", "team", "ahmed_bahaa.jpg")
        if f_ceo:
            ceo.photo.save("ahmed_bahaa.jpg", f_ceo, save=True)

        # Vice Chairman
        vc = TeamMember.objects.create(
            name="Mr. Mahmoud Bahaa",
            position="Vice Chairman / Board Member",
            member_type="executive",
            quote="Building enduring partnerships through operational precision and transparent corporate governance.",
            bio="Overseeing corporate development, joint ventures, and institutional procurement.",
            order=3,
            is_active=True,
        )
        f_vc = self.copy_media_file("img/team/mahmoud-bahaa.jpg", "team", "mahmoud_bahaa.jpg")
        if f_vc:
            vc.photo.save("mahmoud_bahaa.jpg", f_vc, save=True)

        # 5. Careers & Openings
        self.stdout.write("  [5/9] Hydrating Careers Settings, Pillars & Job Openings...")
        career_settings = CareerSettings.load()
        career_settings.spontaneous_eyebrow = "SPONTANEOUS APPLICATION"
        career_settings.spontaneous_title = "Didn't find the right role for you?"
        career_settings.spontaneous_description = "We are constantly seeking passionate engineers, BIM coordinators, and construction managers. Send your CV and portfolio directly to our recruitment team, and we will contact you when a fitting opportunity opens."
        career_settings.spontaneous_btn_text = "Send Your CV"
        career_settings.spontaneous_email = "careers@albahaacontracting.com"
        career_settings.save()

        cp_data = [
            ("01", "Engineering Precision & QA/QC", "We cultivate an environment of uncompromising engineering standards, continuous professional development, and technical rigor on every job site.", 1),
            ("02", "Safety First & Zero-Harm Culture", "Our comprehensive health, safety, and environmental protocols ensure a secure, structured workspace where every team member thrives.", 2),
            ("03", "Career Trajectory & Leadership Growth", "We provide clear career pathways, mentorship from senior project directors, and opportunities to lead multi-million pound national projects.", 3),
        ]
        CareerPillar.objects.all().delete()
        for num, title, desc, o in cp_data:
            CareerPillar.objects.create(number=num, title=title, description=desc, order=o, is_active=True)

        depts_data = [
            ("Site Engineering", "site-engineering", 1),
            ("Technical Office", "technical-office", 2),
            ("QA / QC", "qa-qc", 3),
            ("MEP Operations", "mep-operations", 4),
        ]
        JobDepartment.objects.all().delete()
        dept_objs = {}
        for name, slug, o in depts_data:
            dept_objs[slug] = JobDepartment.objects.create(name=name, slug=slug, order=o)

        jobs_data = [
            ("Senior Infrastructure Project Manager", "senior-infrastructure-project-manager", "site-engineering", "Full-Time", "10-15 Years", "Leading Grade A municipal water, sewage transmission, and major civil works in New Cairo.", "Direct multi-discipline site execution teams and ensure milestone adherence.\nOversee subcontractor performance, QA/QC audits, and safety compliance.\nManage project budgeting, client progress billings, and variation submittals.", "B.Sc. in Civil Engineering from an accredited institution.\nMinimum 10 years of contracting experience in major wet utilities.\nProven track record with Egyptian governmental authorities.", "Competitive executive salary package\nAnnual performance incentive bonus\nComprehensive medical coverage", 1),
            ("Technical Office Lead Engineer", "technical-office-lead-engineer", "technical-office", "Full-Time", "7-10 Years", "Spearheading shop drawing approvals, BIM coordination, and quantity surveying.", "Lead preparation of detailed shop drawings, bar bending schedules, and MEP coordination.\nPerform value engineering reviews and quantify project variations.\nLiaise with lead consultant engineering offices for submittal approvals.", "B.Sc. in Civil or Architectural Engineering.\nProficiency in AutoCAD, Revit, and BIM 360.\nStrong analytical and contract administration capabilities.", "Structured career advancement path\nProfessional training & software certifications\nFamily medical insurance plan", 2),
            ("QA/QC Civil Inspection Manager", "qa-qc-civil-inspection-manager", "qa-qc", "Full-Time", "8-12 Years", "Overseeing structural concrete quality, material submittals, and laboratory testing.", "Establish and enforce the project Quality Management Plan (QMP).\nConduct regular site inspections, audit concrete pours, and witness laboratory tests.\nManage Non-Conformance Reports (NCRs) and oversee corrective actions.", "B.Sc. in Civil Engineering.\nCertified Quality Auditor (CQI/IRCA or ASQ preferred).\nIn-depth knowledge of Egyptian and international building codes.", "Attractive remuneration package\nTransportation allowance\nContinuous professional development", 3),
            ("Electro-Mechanical (MEP) Site Engineer", "electro-mechanical-mep-site-engineer", "mep-operations", "Full-Time", "5-8 Years", "Executing pumping station electromechanical installations and BMS automation.", "Supervise MEP installations including high-capacity pumps, valves, and electrical panels.\nCoordinate electromechanical interfaces with civil concrete structures.\nWitness pre-commissioning pressure tests and system balancing.", "B.Sc. in Mechanical or Electrical Engineering.\n5+ years of experience in water and sewage pumping station MEP.\nFamiliarity with SCADA and automated control systems.", "Performance-linked bonus structure\nComprehensive health and life insurance\nSite allowance and logistical support", 4),
        ]
        JobOpening.objects.all().delete()
        for title, slug, dept_slug, jtype, exp, summ, resp, req, ben, o in jobs_data:
            JobOpening.objects.create(
                title=title,
                slug=slug,
                department=dept_objs[dept_slug],
                location="New Cairo, Egypt",
                job_type=jtype,
                experience=exp,
                summary=summ,
                responsibilities=resp,
                requirements=req,
                benefits=ben,
                is_active=True,
                order=o,
            )

        # 6. Client Logos (All 12) & Testimonials
        self.stdout.write("  [6/9] Hydrating 12 Institutional Client Logos & Testimonials...")
        logos_data = [
            ("New Urban Communities Authority (NUCA)", "img/clients/Layer 1.png", 1),
            ("National Authority for Potable Water & Sanitary Drainage (NOPWASD)", "img/clients/Layer 2.png", 2),
            ("Armed Forces Engineering Authority", "img/clients/Layer 3.png", 3),
            ("Arab Contractors (Osman Ahmed Osman)", "img/clients/Layer 4.png", 4),
            ("Arab Consulting Engineers (ACE - Moharram Bakhoum)", "img/clients/Layer 5.png", 5),
            ("Dar Al-Handasah Consultants", "img/clients/Layer 6.png", 6),
            ("Consulting Engineers Group (CEG)", "img/clients/l3.png", 7),
            ("Prime Developments Egypt", "img/clients/logo_partner-3.png", 8),
            ("Egyptian Federation for Construction Contractors", "img/clients/11.png", 9),
            ("Corporate Architectural Development Partners", "img/clients/logo_partner-8.png", 10),
            ("Civil Engineering Supervision Council", "img/clients/l4.png", 11),
            ("National Housing & Utilities Authority", "img/clients/Layer 1 copy.png", 12),
        ]
        ClientLogo.objects.all().delete()
        for name, img_path, o in logos_data:
            logo = ClientLogo.objects.create(name=name, order=o, show_on_home=True, show_on_about=True, is_active=True)
            f_logo = self.copy_media_file(img_path, "clients", f"client_{o}.png")
            if f_logo:
                logo.logo_image.save(f"client_{o}.png", f_logo, save=True)

        testimonials_data = [
            ("Consulting Engineers Group (CEG)", "Supervising Engineering Committee", "Major Infrastructure Division", "Al Bahaa demonstrated impeccable technical rigor, Grade A compliance, and flawless coordination on critical municipal infrastructure networks.", False, 1),
            ("Urban Communities Authority", "Infrastructure Sector Director", "Cairo Regional Office", "Their adherence to structural milestones, safety protocols, and quality control sets an industry benchmark for joint-stock contractors in Egypt.", False, 2),
            ("Prime Developments", "Executive Board Director", "Commercial Landmarks Group", "Working with Al Bahaa provided absolute peace of mind. Turnkey project delivery executed on schedule with outstanding attention to engineering QA/QC.", True, 3),
        ]
        Testimonial.objects.all().delete()
        for cname, pos, comp, quote, is_acc, o in testimonials_data:
            Testimonial.objects.create(
                client_name=cname,
                position=pos,
                company=comp,
                quote=quote,
                is_accent=is_acc,
                is_featured=is_acc,
                show_on_home=True,
                show_on_about=True,
                order=o,
            )

        # 7. Projects & Galleries
        self.stdout.write("  [7/9] Hydrating 5 Landmark Projects & Galleries...")
        categories_data = [
            ("Water & Sewage Infrastructure", "water-sewage", 1),
            ("Commercial & Business Hubs", "commercial", 2),
            ("Administrative & Institutional", "administrative", 3),
            ("Civil & Heavy Structural Works", "civil-structural", 4),
        ]
        ProjectCategory.objects.all().delete()
        cat_objs = {}
        for cname, cslug, o in categories_data:
            cat_objs[cslug] = ProjectCategory.objects.create(name=cname, slug=cslug, order=o)

        projects_data = [
            (
                "Eastern Al-Ma'abda Sewerage System & Pumping Stations",
                "eastern-al-maabda-sewerage",
                "water-sewage",
                "Assiut, Egypt",
                "National Authority for Potable Water & Sanitary Drainage (NOPWASD)",
                "Dar Al-Handasah Consultants",
                "Turnkey Infrastructure Contracting & Commissioning",
                "completed",
                "2026-06-15",
                "350,000 LM Network Scale",
                "A flagship municipal infrastructure project delivering vital sanitation networks, pressurized force mains, and high-efficiency pumping stations.",
                "The Eastern Al-Ma'abda development is a landmark civil undertaking engineered to resolve long-standing wastewater management requirements in Upper Egypt.\nExecuted under stringent Grade A standards, the project encompassed extensive deep-trench excavations, microtunneling under key regional transit corridors, and the construction of reinforced concrete pumping facilities engineered with sulfate-resistant cement and waterproof containment membranes.\nIntegrated electro-mechanical systems feature automated SCADA telemetry, dual backup generator sets, and self-cleaning wet well pumps delivering continuous, fault-tolerant operation.",
                "BIM 3D modeling and multidisciplinary MEP clash coordination prior to site execution.\nInstallation of heavy-duty vitrified clay (VCP) and high-density polyethylene (HDPE) pipelines.\nReinforced concrete pump station substructure cast with zero-permeability waterproofing additives.\nAutomated SCADA telemetry with real-time level sensing and fault diagnostics.\nComprehensive hydro-testing of all network segments at 1.5x operating pressure before handover.",
                "Significantly mitigates local groundwater contamination and enhances sanitation security for over 120,000 regional residents.",
                "img/projects/projects-band-1-recovered.png",
                "project_1.png",
                True,
                1,
            ),
            (
                "Administrative Capital Commercial Hub & Executive Tower",
                "administrative-capital-hub",
                "commercial",
                "New Administrative Capital, Egypt",
                "Prime Urban Developments",
                "Arab Consulting Engineers (ACE - Moharram Bakhoum)",
                "Full Civil, Structural Concrete & High-End Shell Construction",
                "in_progress",
                "2026-12-30",
                "65,000 m² BUA",
                "A premier commercial and administrative multi-use landmark featuring high-performance structural framing and post-tensioned slabs.",
                "Positioned at the heart of the New Administrative Capital financial district, this 14-story commercial center combines Grade A corporate office spaces with luxury retail arcades.\nAl Bahaa's engineering scope encompasses deep foundation piling, diaphragm retaining wall execution, post-tensioned structural slabs, and seamless MEP rough-in coordination.",
                "Post-tensioned concrete slab systems maximizing open column-free floor spans.\nDiaphragm retaining wall and deep piling executed with high-precision CFA rigs.\nBIM Level 2 coordination for electromechanical routing and architectural facade embeds.",
                "Engineered for EDGE Green Building standards with solar-ready roof embeds and energy-efficient building envelopes.",
                "img/projects/projects-band-2-recovered.png",
                "project_2.png",
                True,
                2,
            ),
            (
                "New Cairo Central Water Transmission Pipeline",
                "new-cairo-water-pipeline",
                "water-sewage",
                "First Settlement, New Cairo, Egypt",
                "New Urban Communities Authority (NUCA)",
                "Consulting Engineers Group (CEG)",
                "Ductile Iron Pipeline Transmission Network & Valve Chambers",
                "completed",
                "2025-11-20",
                "45,000 LM Main Line",
                "High-capacity potable water transmission corridor engineered with 1200mm ductile iron pipelines to secure regional urban supply.",
                "A strategic water transmission network connecting major treatment facilities to newly developed urban settlements across East Cairo.\nWorks included trenchless microtunneling beneath existing arterial ring roads and precision installation of air-release and sectional gate valve chambers.",
                "1200mm Class K9 ductile iron transmission pipes with internal cement mortar lining.\nTrenchless horizontal directional drilling (HDD) under major transportation arteries.\nCast-in-place reinforced concrete valve chambers equipped with telemetry monitoring.",
                "Secures clean potable water distribution for expanding municipal communities with zero pipeline leakage benchmarks.",
                "img/projects/projects-band-3-recovered.png",
                "project_3.png",
                True,
                3,
            ),
            (
                "Industrial Logistics Warehouse & Logistics Facility",
                "industrial-logistics-facility",
                "civil-structural",
                "10th of Ramadan City, Egypt",
                "National Logistics Corporation",
                "Civil Engineering Supervision Group",
                "Turnkey Structural Steel & Reinforced Concrete Logistics Center",
                "completed",
                "2025-08-10",
                "42,000 m² Facility",
                "Heavy-duty logistical warehouse engineered with laser-leveled super-flat concrete floors and clear-span steel portals.",
                "Constructed to support high-throughput industrial logistics, featuring heavy vehicle loading bays, reinforced concrete aprons, and integrated fire suppression pumping infrastructure.",
                "Super-flat laser screed concrete flooring engineered for heavy forklift loading.\nClear-span 36m structural steel portal frames fabricated to strict deflection tolerances.\nDedicated fire-fighting reservoir and automated deluge sprinkler system.",
                "Equipped with LED high-bay smart illumination and rainwater harvesting drainage infrastructure.",
                "img/projects/projects-band-4-recovered.png",
                "project_4.png",
                False,
                4,
            ),
            (
                "Urban Residential Gated Enclave & Infrastructure Works",
                "urban-residential-enclave",
                "administrative",
                "New Cairo, Egypt",
                "Cairo Real Estate Investment S.A.E",
                "Architectural & Engineering Consulting Bureau",
                "Integrated Civil Infrastructure, Roadworks & Utilities",
                "in_progress",
                "2026-11-15",
                "180,000 m² Master Development",
                "Turnkey residential master-plan infrastructure including internal road grading, stormwater drainage, and subterranean electrical network.",
                "A comprehensive residential infrastructure package integrating subterranean power networks, fiber optic ducting, landscaped utility corridors, and asphalt road networks.",
                "Integrated underground utility corridors minimizing surface disruption.\nPermeable pavement and stormwater percolation drainage systems.\nPrecision asphalt paving and curbside civil landscaping.",
                "High-permeability surface drainage recharging regional sub-surface reservoirs.",
                "img/projects/project-detail-tower-recovered.png",
                "project_5.png",
                False,
                5,
            ),
        ]
        Project.objects.all().delete()
        ProjectImage.objects.all().delete()

        gallery_static_files = [
            "img/projects/Rectangle 24 copy 2     .png",
            "img/projects/Rectangle 24 copy 3   .png",
            "img/projects/Rectangle 24 copy 6.png",
            "img/projects/Rectangle 9 copy.png",
        ]

        for ptitle, pslug, cslug, loc, client, consult, scope, stat, dt, scale, sdesc, fdesc, hl, sust, cover_src, out_cover, is_feat, o in projects_data:
            proj = Project.objects.create(
                title=ptitle,
                slug=pslug,
                category=cat_objs[cslug],
                location=loc,
                client_name=client,
                architect_consultant=consult,
                scope_of_work=scope,
                status=stat,
                date=dt,
                built_up_area=scale,
                short_description=sdesc,
                full_description=fdesc,
                engineering_highlights=hl,
                sustainability=sust,
                is_featured=is_feat,
                order=o,
            )
            f_proj_cover = self.copy_media_file(cover_src, "projects", out_cover)
            if f_proj_cover:
                proj.cover_image.save(out_cover, f_proj_cover, save=True)

            # Seed 2-3 Project Images for Gallery
            for g_idx, g_file in enumerate(gallery_static_files[:3]):
                g_out_name = f"gallery_{pslug}_{g_idx+1}.png"
                f_gal = self.copy_media_file(g_file, "projects/gallery", g_out_name)
                if f_gal:
                    p_img = ProjectImage(project=proj, caption=f"Execution Milestone {g_idx+1} - {ptitle}", order=g_idx+1)
                    p_img.image.save(g_out_name, f_gal, save=True)

        # 8. News Categories & Articles
        self.stdout.write("  [8/9] Hydrating 6 Technical Articles & Categories...")
        news_cats_data = [
            ("Infrastructure", "infrastructure", 1),
            ("Civil Works", "civil-works", 2),
            ("Sustainability", "sustainability", 3),
            ("Corporate Governance", "corporate", 4),
            ("Tenders & Awards", "tenders", 5),
            ("Engineering Rigor", "engineering", 6),
        ]
        NewsCategory.objects.all().delete()
        ncat_objs = {}
        for ncname, ncslug, o in news_cats_data:
            ncat_objs[ncslug] = NewsCategory.objects.create(name=ncname, slug=ncslug, order=o)

        articles_data = [
            (
                "Advancing Egypt's Water & Municipal Transmission Networks",
                "advancing-egypts-water-infrastructure-networks",
                "infrastructure",
                "Eng. Ahmed Bahaa (CEO)",
                "Al Bahaa expands its Grade A infrastructure division, implementing modern trenchless piping and automated pump station technologies across major national initiatives.",
                "Municipal water security represents the cornerstone of modern urban expansion in Egypt. As an active Grade A contractor accredited by the Egyptian Federation for Construction, Al Bahaa has continuously pioneered advanced pipe-laying methodologies, precision microtunneling, and automated SCADA pump stations.\nOur technical teams collaborate directly with public utility authorities, ensuring that every kilometer of potable water and sanitary drainage meets rigorous QA/QC standards and long-term durability metrics.\nThrough strategic investments in specialized trenching machinery and BIM coordination, Al Bahaa delivers critical infrastructure projects on schedule and within budget.",
                "2026-10-15 10:00:00",
                "img/news/news-article1-recovered.png",
                "article_1.png",
                1,
            ),
            (
                "Pioneering Quality Control & Structural Milestones in High-Rise Foundations",
                "quality-control-structural-milestones-high-rise",
                "civil-works",
                "Technical Office & QA/QC Committee",
                "Achieving zero-defect concrete pours on high-capacity administrative structures using advanced QA/QC monitoring and thermographic inspection.",
                "Mass concrete foundation casting demands meticulous thermal control, slump monitoring, and automated curing protocols. On our recent administrative tower developments, our engineering teams instituted comprehensive continuous sensor monitoring to track hydration heat gradients and prevent thermal cracking.\nEvery batch of high-strength concrete is sampled and laboratory-tested across 7, 28, and 56-day compressive intervals, maintaining an unyielding zero-defect standard across structural works.",
                "2026-09-28 11:30:00",
                "img/news/news-article2-recovered.png",
                "article_2.png",
                2,
            ),
            (
                "Sustainable High-Performance Facade Engineering in Modern Corporate Landmarks",
                "sustainable-facade-engineering-corporate-landmarks",
                "sustainability",
                "Eng. Mahmoud Bahaa (Vice Chairman)",
                "Integrating climate-resilient envelope technologies, low-E glazing, and solar shading into landmark urban developments across Egypt.",
                "Sustainable contracting is no longer an optional feature—it is a core engineering requirement. Al Bahaa integrates lifecycle value engineering into architectural facades, utilizing thermal-break aluminum profiles, high-performance double glazing, and localized solar shading to reduce building cooling loads by up to 30%.\nThese engineering initiatives align with Egypt's Vision 2030 green building benchmarks and provide enduring operational savings for developers.",
                "2026-08-14 09:15:00",
                "img/news/news-article3-recovered.png",
                "article_3.png",
                3,
            ),
            (
                "BIM 3D Modeling & MEP Clash Coordination in Complex Contracting",
                "bim-3d-modeling-mep-clash-coordination",
                "engineering",
                "BIM & Technical Office Team",
                "How digital twin workflows and pre-construction clash resolution reduce on-site variations and optimize project schedules.",
                "Prior to pouring a single cubic meter of structural concrete, Al Bahaa's digital engineering department develops comprehensive Level 2 BIM models. By resolving interferences between electromechanical ducting, high-pressure piping, and post-tensioned structural slabs in the virtual model, we virtually eliminate on-site rework, saving significant time and material resources.",
                "2026-07-20 14:00:00",
                "img/news/news-article1-recovered.png",
                "article_4.png",
                4,
            ),
            (
                "Occupational Safety & Zero-Harm Protocols on Active Infrastructure Sites",
                "occupational-safety-zero-harm-protocols",
                "corporate",
                "HSE Supervision Directorate",
                "Enforcing stringent occupational health and safety benchmarks across civil and utility job sites nationwide.",
                "Safety is the fundamental pillar upon which Al Bahaa's operational excellence is built. With daily toolbox talks, certified safety officers on every active site, and strict PPE enforcement, we have achieved over 2 million safe work hours across our landmark developments. Our zero-harm protocol safeguards our workforce and surrounding communities.",
                "2026-06-10 08:45:00",
                "img/news/news-article2-recovered.png",
                "article_5.png",
                5,
            ),
            (
                "Al Bahaa Awarded Major Municipal Infrastructure Expansion Project",
                "al-bahaa-awarded-major-infrastructure-expansion",
                "tenders",
                "Business Development & Tenders Office",
                "New contract award encompassing extensive potable water network distribution and collector mainlines in New Cairo.",
                "Al Bahaa Contracting has been formally awarded the execution of comprehensive municipal water transmission and sanitary drainage networks in East Cairo. The project scope includes 45 kilometers of high-grade ductile iron piping, automated valve chambers, and turn-key handover within 18 calendar months.",
                "2026-05-02 12:00:00",
                "img/news/news-article3-recovered.png",
                "article_6.png",
                6,
            ),
        ]
        Post.objects.all().delete()
        for atitle, aslug, acatslug, aauth, aexc, acont, apub, cimg, out_img, o in articles_data:
            post_obj = Post.objects.create(
                title=atitle,
                slug=aslug,
                category=ncat_objs[acatslug],
                author=aauth,
                excerpt=aexc,
                content=acont,
                published_at=apub,
                is_published=True,
                order=o,
            )
            f_post = self.copy_media_file(cimg, "news", out_img)
            if f_post:
                post_obj.cover_image.save(out_img, f_post, save=True)

        # 9. RBAC Groups Setup
        self.stdout.write("  [9/9] Configuring Corporate RBAC User Groups...")
        # Group 1: HR & Recruitment
        hr_group, _ = Group.objects.get_or_create(name="HR & Recruitment")
        job_ct = ContentType.objects.get_for_model(JobOpening)
        app_ct = ContentType.objects.get_for_model(JobApplication)
        hr_perms = Permission.objects.filter(content_type__in=[job_ct, app_ct])
        hr_group.permissions.set(hr_perms)

        # Group 2: Media & Content Editors
        media_group, _ = Group.objects.get_or_create(name="Media & Content Editors")
        post_ct = ContentType.objects.get_for_model(Post)
        proj_ct = ContentType.objects.get_for_model(Project)
        test_ct = ContentType.objects.get_for_model(Testimonial)
        media_perms = Permission.objects.filter(content_type__in=[post_ct, proj_ct, test_ct])
        media_group.permissions.set(media_perms)

        # Group 3: Technical Office & Tenders
        tenders_group, _ = Group.objects.get_or_create(name="Technical Office & Tenders")
        contact_ct = ContentType.objects.get_for_model(ContactMessage)
        tenders_perms = Permission.objects.filter(content_type=contact_ct)
        tenders_group.permissions.set(tenders_perms)

        # Clear Cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS(">>> [SUCCESS] 100% CMS DATA & MEDIA HYDRATION COMPLETED SUCCESSFULLY!"))
