import os
import matplotlib.pyplot as plt
import matplotlib
from gvxrPython3 import gvxr
import numpy as np
class XRaySimulation:
    """
    A class to simulate X-ray imaging of anatomical models.
    
    Supports simulation with different model thicknesses and configurations.
    """
    
    def __init__(self, thickness_type='small', tube_voltage=80):
        """
        Initialize the X-ray simulation.
        
        Args:
            thickness_type (str): Type of model thickness. 
                                  Options: 'small' or 'large'.
        """
        # Validate input
        if thickness_type.lower() not in ['small', 'large']:
            raise ValueError("thickness_type must be 'small' or 'large'")
        
        self.thickness_type = thickness_type.lower()
        self.tube_voltage = tube_voltage
        
        # Configure matplotlib
        self._configure_matplotlib()
        
        # Set model paths and names based on thickness
        self._set_model_paths()
    
    def _set_model_paths(self):
        """
        Set model file paths and names based on thickness type.
        """
        base_path = "Data"
        if self.thickness_type == 'small':
            self.fname_torso = os.path.join(base_path, "TORSO_Small.stl")
            self.fname_pelvis = os.path.join(base_path, "PELVIS_Small.stl")
            self.torso_name = "TORSO_Small"
            self.pelvis_name = "PELVIS_Small"
        else:  # large
            self.fname_torso = os.path.join(base_path, "TORSO_Large.stl")
            self.fname_pelvis = os.path.join(base_path, "PELVIS_Large.stl")
            self.torso_name = "TORSO_Large"
            self.pelvis_name = "PELVIS_Large"

    def _configure_matplotlib(self):
        """Configure matplotlib font settings."""
        font = {
            'family': 'serif',
            'size': 15
        }
        matplotlib.rc('font', **font)
    
    def setup_x_ray_source(self):
        """Configure the X-ray source parameters."""
        if self.thickness_type == 'small':
            gvxr.setSourcePosition(-5.0, 0.0, 0.0, "cm")
        else:
            gvxr.setSourcePosition(-20.0, 1.7, 0.0, "cm")
        
        gvxr.usePointSource()
        
        # Set monochromatic beam
        gvxr.setMonoChromatic(self.tube_voltage, "keV", 1000)
    
    def setup_detector(self):
        """Configure the X-ray detector parameters."""
        if self.thickness_type == 'small':
            gvxr.setDetectorPosition(10.0, 0.0, 0.0, "cm")
            gvxr.setDetectorNumberOfPixels(500, 430)
        else:
            gvxr.setDetectorPosition(20.0, 0.0, 0.0, "cm")
            gvxr.setDetectorNumberOfPixels(1200, 1200)
        
        gvxr.setDetectorUpVector(0, 0, -1)
        gvxr.setDetectorPixelSize(0.5, 0.5, "mm")
    
    def load_and_position_models(self):
        """
        Load and position anatomical models based on thickness type.
        """
        gvxr.removePolygonMeshesFromSceneGraph()
        # Load mesh files
        gvxr.loadMeshFile(self.torso_name, self.fname_torso, "mm")
        gvxr.loadMeshFile(self.pelvis_name, self.fname_pelvis, "mm")
        
        # Move models to centre
        gvxr.moveToCentre(self.torso_name)
        gvxr.moveToCentre(self.pelvis_name)
        
        # Translate models
        if self.thickness_type == 'small':
            translate_offset = 1.3
            gvxr.translateNode(self.pelvis_name, 0, translate_offset, -10, "mm")
            gvxr.translateNode(self.torso_name, 0, 0, -10, "mm")
        else:
            translate_offset = 3.0
            gvxr.translateNode(self.pelvis_name, -40, translate_offset, -40, "mm")
            gvxr.translateNode(self.torso_name, -40, 0, -40, "mm")
        
        # Rotate models
        gvxr.rotateNode(self.torso_name, -90, 0, 0, 1)
        gvxr.rotateNode(self.pelvis_name, -90, 0, 0, 1)
    
    def set_material_properties(self):
        """
        Set material properties for anatomical models.
        """
        # Soft tissue (mostly water)
        gvxr.setCompound(self.torso_name, "H2O")
        gvxr.setDensity(self.torso_name, 1.03, "g/cm3")
        
        # Bone (Hydroxyapatite approximation)
        gvxr.setCompound(self.pelvis_name, "Ca10(PO4)6(OH)2")
        gvxr.setDensity(self.pelvis_name, 1.92, "g/cm3")
    
    def simulate_x_ray(self):
        """
        Simulate X-ray image and visualize results.
        
        Returns:
            numpy.ndarray: The computed X-ray image
        """
        # Create OpenGL context
        gvxr.createOpenGLContext()
        
        # Setup X-ray components
        self.setup_x_ray_source()
        self.setup_detector()
        
        # Load and position models
        self.load_and_position_models()
        
        # Set material properties
        self.set_material_properties()
        
        # Compute X-ray image
        print(f"Computing X-ray image for {self.thickness_type} thickness models...")
        x_ray_image = gvxr.computeXRayImage()
        
        return x_ray_image
    
    def visualize_x_ray(self, x_ray_image):
        """
        Visualize the X-ray image.
        
        Args:
            x_ray_image (numpy.ndarray): The X-ray image to visualize
        """
        plt.figure(figsize=(15, 7.5))
        plt.suptitle(f"(Relatively {self.thickness_type.capitalize()} Thickness) \n(Tube Voltage: {self.tube_voltage} KeV)", y=0.5)

        
        plt.subplot(131)
        plt.imshow(x_ray_image, cmap="gray")
        # plt.imshow(np.subtract(255, x_ray_image), cmap="gray")
        plt.colorbar(orientation='horizontal')
        plt.title("Linear Color Scale")
        
        plt.tight_layout()
        plt.show()
    
    def run(self):
        """
        Run the complete X-ray simulation and visualization.
        """
        x_ray_image = self.simulate_x_ray()
        self.visualize_x_ray(x_ray_image)

def main():
    """Main function to demonstrate X-ray simulation."""
    # Simulate with small thickness models
    small_thickness_sim = XRaySimulation(thickness_type='small')
    small_thickness_sim.run()
    
    # Simulate with large thickness models
    large_thickness_sim = XRaySimulation(thickness_type='large')
    large_thickness_sim.run()

if __name__ == "__main__":
    main()