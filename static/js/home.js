/**
 * Al Bahaa Home Page Interactions
 * Handles the interactive Specializations switcher dynamically from Django context.
 */
document.addEventListener("DOMContentLoaded", () => {
  const fallbackData = [
    {
      discipline: "GRADE A INFRASTRUCTURE",
      title: "Municipal Water Transmission & Collector Networks",
      description: "Specialized in municipal water transmission pipelines, sewage collector networks, pumping stations, and stormwater drainage systems engineered to exacting standards."
    },
    {
      discipline: "CIVIL & STRUCTURAL WORKS",
      title: "Heavy Reinforced Concrete & Deep Foundations",
      description: "Heavy reinforced concrete structures, deep foundation earthworks, structural steel framing, and institutional facilities built for enduring durability."
    },
    {
      discipline: "TURNKEY GENERAL CONTRACTING",
      title: "Commercial & Residential Landmarks",
      description: "Comprehensive end-to-end project execution from initial site earthworks and BIM coordination to high-end architectural finishes delivered on schedule."
    },
    {
      discipline: "ELECTROMECHANICAL & MEP",
      title: "Integrated MEP, BMS & Substation Engineering",
      description: "Advanced electro-mechanical installations, automated pump station control, value engineering, and high-efficiency MEP infrastructure."
    }
  ];

  let specializationData = fallbackData;
  const scriptTag = document.getElementById("specializations-data");
  if (scriptTag) {
    try {
      const parsed = JSON.parse(scriptTag.textContent);
      if (Array.isArray(parsed) && parsed.length > 0) {
        specializationData = parsed;
      }
    } catch (e) {
      console.warn("Could not parse specializations data script, using default fallback.", e);
    }
  }

  const specContainer = document.querySelector(".home-specialization");
  if (!specContainer) return;

  const disciplineEl = specContainer.querySelector(".home-specialization__discipline");
  const descEl = specContainer.querySelector(".home-specialization__desc");
  const prevBtn = specContainer.querySelector(".home-specialization__previous");
  const nextBtn = specContainer.querySelector(".home-specialization__next");

  if (!disciplineEl || !descEl || !prevBtn || !nextBtn) return;

  let currentIndex = 0;

  function updateSpecialization(index) {
    currentIndex = (index + specializationData.length) % specializationData.length;
    const item = specializationData[currentIndex];

    // Subtle smooth text update
    disciplineEl.style.opacity = "0";
    descEl.style.opacity = "0";

    setTimeout(() => {
      disciplineEl.textContent = item.discipline || item.title || "";
      descEl.textContent = item.description || "";
      disciplineEl.style.opacity = "1";
      descEl.style.opacity = "1";
    }, 140);
  }

  // Ensure initial transitions are ready
  disciplineEl.style.transition = "opacity 140ms ease";
  descEl.style.transition = "opacity 140ms ease";

  prevBtn.addEventListener("click", () => {
    updateSpecialization(currentIndex - 1);
  });

  nextBtn.addEventListener("click", () => {
    updateSpecialization(currentIndex + 1);
  });
});
