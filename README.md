# X-ray Image Simulator

## Overview

This project models how X-rays are attenuated as they pass through different tissues such as bone, soft tissue, and air. The simulation is based on exponential decay of X-ray intensity and considers tissue-specific interactions like photoelectric absorption and Compton scattering. The study also explores how beam energy and tissue thickness impact attenuation and image contrast.

## Objectives

- Model X-ray beam attenuation through various human tissues.
- Analyze the impact of beam energy and tissue type on attenuation.
- Simulate X-ray imaging using anatomical 3D models.
- Visualize differences in image contrast under varying conditions.

## Methodology

### 1. Attenuation Model

- **Linear Attenuation Coefficient (μ):**  
  Computed as:  
  `μ = mass attenuation coefficient × material density`

- **Exponential Decay Formula:**  
  `I = I₀ * e^(-μx)`  
  where:
  - *I₀* is the initial X-ray intensity  
  - *μ* is the linear attenuation coefficient  
  - *x* is the thickness of the material  

### 2. X-ray Interactions

- **Photoelectric Absorption:** Dominant in bone, especially at low energy.
- **Compton Scattering:** Predominant in soft tissues at medium energy levels.

### 3. Tissue-Specific Attenuation

- **Bone:** High attenuation at low energy due to high density and atomic number.
- **Air:** Minimal attenuation due to low density.
- **Soft Tissue:** Moderate attenuation depending on energy and thickness.

### 4. Layered Tissue Simulation (0.1 MeV)

- Demonstrated cumulative attenuation from air, soft tissue, and bone in sequence.

### 5. X-ray Imaging Simulation

- **3D Modeling:** Pelvic region modeled in Blender.
- **Simulation Tool:** GVXR Python library.
- **Scenarios Tested:**
  - Varying tissue thicknesses.
  - Varying X-ray energies (e.g., 30 keV vs 150 keV).

## Tools & Libraries

- Python
- GVXR library
- Blender (3D anatomical modeling)
- Matplotlib (for plots)

## Results

- X-ray attenuation visualized across tissue types and energies.
- Simulations showed clear contrasts in imaging based on material and beam properties.
- Images reveal stronger absorption in bone and low transmission in soft tissue at low energies.


