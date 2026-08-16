/**
 * Al Bahaa Home Page Interactions
 * Handles the interactive Specializations switcher smoothly and reliably.
 */
document.addEventListener("DOMContentLoaded", () => {
  const specializationData = [
    {
      title: "GRADE A INFRASTRUCTURE",
      description: "Specialized in municipal water transmission pipelines, sewage collector networks, pumping stations, and stormwater drainage systems engineered to exacting standards."
    },
    {
      title: "CIVIL & STRUCTURAL WORKS",
      description: "Heavy reinforced concrete structures, deep foundation earthworks, structural steel framing, and institutional facilities built for enduring durability."
    },
    {
      title: "TURNKEY GENERAL CONTRACTING",
      description: "Comprehensive end-to-end project execution from initial site earthworks and BIM coordination to high-end architectural finishes delivered on schedule."
    },
    {
      title: "ELECTROMECHANICAL & MEP",
      description: "Advanced electro-mechanical installations, automated pump station control, value engineering, and high-efficiency MEP infrastructure."
    }
  ];

  const specContainer = document.querySelector(".home-specialization");
  if (!specContainer) return;

  const titleEl = specContainer.querySelector(".home-specialization__discipline");
  const descEl = specContainer.querySelector(".home-specialization__desc");
  const prevBtn = specContainer.querySelector(".home-specialization__previous");
  const nextBtn = specContainer.querySelector(".home-specialization__next");

  if (!titleEl || !descEl || !prevBtn || !nextBtn) return;

  let currentIndex = 0;

  function updateSpecialization(index) {
    currentIndex = (index + specializationData.length) % specializationData.length;
    const item = specializationData[currentIndex];

    // Subtle smooth text update
    titleEl.style.opacity = "0";
    descEl.style.opacity = "0";

    setTimeout(() => {
      titleEl.textContent = item.title;
      descEl.textContent = item.description;
      titleEl.style.opacity = "1";
      descEl.style.opacity = "1";
    }, 140);
  }

  // Ensure initial transitions are ready
  titleEl.style.transition = "opacity 140ms ease";
  descEl.style.transition = "opacity 140ms ease";

  prevBtn.addEventListener("click", () => {
    updateSpecialization(currentIndex - 1);
  });

  nextBtn.addEventListener("click", () => {
    updateSpecialization(currentIndex + 1);
  });
});
