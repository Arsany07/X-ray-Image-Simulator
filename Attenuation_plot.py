import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from scipy.interpolate import interp1d

class XRayAttenuationPlot:
    def __init__(self):
        """
        Initialize XRay Attenuation Plot with default material properties.
        """
        self.energies_data = np.array([0.01, 0.1, 1, 10, 20])
        self.mac = {
            "bone": np.array([28.51, 0.1855, 0.0656, 0.02314, 0.02068]),
            "soft_tissue": np.array([4.937, 0.1688, 0.07003, 0.02191, 0.01785]),
            "air": np.array([5.120, 0.1541, 0.06358, 0.02045, 0.01705])
        }
        self.densities = {"bone": 1.92, "soft_tissue": 1.03, "air": 0.001225}
        
        # Create interpolation functions for each material
        self.interp_funcs = {
            mat: interp1d(self.energies_data, data, kind='linear', fill_value='extrapolate') 
            for mat, data in self.mac.items()
        }

    def get_linear_attenuation_coefficient(self, material, energy):
        """
        Calculate the linear attenuation coefficient for a given material at a given energy.

        Parameters
        ----------
        material : str
            The name of the material (e.g. "bone", "soft_tissue", "air")
        energy : float
            The energy level in MeV

        Returns
        -------
        The linear attenuation coefficient in cm^-1
        """
        if material not in self.mac:
            raise ValueError(f"Unknown material: {material}")

        # Interpolate mass attenuation coefficient
        mac_value = self.interp_funcs[material](energy)
        
        # Calculate linear attenuation coefficient
        return mac_value * self.densities[material]
    
    def transmitted_intensity(self, I0, mu, thickness):
        """
        Calculate the transmitted intensity of an X-ray beam after passing through a material.

        Parameters
        ----------
        I0 : float
            The initial intensity of the X-ray beam.
        mu : float
            The linear attenuation coefficient of the material (in cm^-1).
        thickness : array-like
            The thickness of the material (in cm).

        Returns
        -------
        array
            The transmitted intensity of the X-ray beam.
        """
        I = I0 * np.exp(-mu * thickness)
        return I
    
    def plot_attenuation(self, material_names, energy_levels, colors, I0, thicknesses):
        """
        Generates and displays plots of X-ray attenuation for various materials and energy levels.

        Parameters
        ----------
        material_names : dict
            A dictionary mapping material identifiers to display names (e.g., {"bone": "Bone"}).
        energy_levels : list
            A list of energy levels (in MeV) for which to calculate and plot attenuation.
        colors : list
            A list of colors for the plot lines corresponding to each energy level.
        I0 : float
            The initial intensity of the X-ray beam.
        thicknesses : array-like
            An array of material thicknesses (in cm) over which to calculate and plot transmitted intensity.
        """
        # Create a plot for each material
        for material, display_name in material_names.items():
            plt.figure(figsize=(10, 6))

            # Plot for each energy level
            for energy, color in zip(energy_levels, colors):
                # Calculate linear attenuation coefficient for this specific energy
                mu = self.get_linear_attenuation_coefficient(material, energy)
                
                # Calculate transmitted intensity
                I_trans = self.transmitted_intensity(I0, mu, thicknesses)
                
                # Plot
                plt.plot(thicknesses, I_trans, color=color, label=f'{energy} MeV')

            plt.xlabel(f"{display_name} Thickness (cm)")
            plt.ylabel("Normalized Transmitted Intensity")
            plt.title(f"X-ray Attenuation through {display_name}")
            plt.legend(title="Energy")
            plt.grid(True)
            plt.tight_layout()
            plt.show()


    def compute_layer_boundaries(self, layers, energy, I0=1000):
        """
        Compute the X-ray intensity at the boundaries of each layer.
        Returns two arrays: positions of the boundaries and the corresponding X-ray intensities.
        """

        I_current = I0
        positions = [0]
        intensities = [I_current]

        for tissue, thick in layers:
            mu = self.get_linear_attenuation_coefficient(tissue, energy)
            I_current = self.transmitted_intensity(I_current, mu, thick)
            positions.append(positions[-1] + thick)
            intensities.append(I_current)

        return positions, intensities

    
    def compute_continuous_attenuation(self, layers, I0=1000, points_per_layer=50):
        """
        Compute the X-ray intensity at a fine grid of points within each layer,
        resulting in a continuous attenuation curve.
        
        Parameters
        ----------
        layers : list
            A list of (tissue, thickness) tuples.
        I0 : float, optional
            The initial intensity of the X-ray beam.
        points_per_layer : int, optional
            The number of points within each layer at which to compute the X-ray intensity.
        
        Returns
        -------
        Two lists: the positions of the points at which the X-ray intensity was computed,
        and the corresponding X-ray intensities.
        """

        positions_cont = []
        intensities_cont = []
        I_current = I0
        current_pos = 0
        energy = self.energies_data[1]
        for tissue, thick in layers:
            pos = np.linspace(current_pos, current_pos + thick, points_per_layer)
            mu = self.get_linear_attenuation_coefficient(tissue, energy)
            intensity = [self.transmitted_intensity(I_current, mu, p - current_pos) for p in pos]
            positions_cont.extend(pos)
            intensities_cont.extend(intensity)
            I_current = intensity[-1]
            current_pos += thick
        
        return positions_cont, intensities_cont
    
    def plot_layered_attenuation_plotly(self, layers, colors, energy, I0=1000):
        """
        Plot both the boundary intensities and a continuous attenuation curve
        for the given layered structure.
        """
    
        positions_cont, intensities_cont = self.compute_continuous_attenuation(layers, I0)
        
        fig = go.Figure()

        # continuous attenuation curve
        fig.add_trace(go.Scatter(
            x=positions_cont,
            y=intensities_cont,
            mode='lines',
            name='Continuous Attenuation',
            line=dict(color='blue', width=3)
        ))

        current_pos = 0
        for tissue, thick in layers:
            # colored rectangle for each layer
            fig.add_shape(
                type='rect',
                x0=current_pos,
                x1=current_pos + thick,
                y0=0,
                y1=I0,
                fillcolor=colors[tissue],
                opacity=0.3,
                layer='below',
                line_width=0
            )

            # annotation for each layer
            fig.add_annotation(
                x=(current_pos + current_pos + thick) / 2,
                y=I0 * 0.5,
                text=tissue.replace('_', ' ').title(),
                showarrow=False
            )

            current_pos += thick

        fig.update_layout(
            title=f"X-ray Attenuation Through Layered Tissues ({energy} MeV)",
            xaxis_title="Depth (cm)",
            yaxis_title="Intensity (% of initial)",
            height=600,
            width=800,
            template='plotly_white'
        )

        fig.show()
    
