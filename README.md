# India Space Academy Internship Projects

This repository contains the Jupyter notebooks and associated files for two projects completed during my internship at the India Space Academy. These projects explore fundamental concepts in astrophysics and cosmology, utilizing observational data and Python-based analysis.

## Projects Overview

1.  **Dynamical Mass Calculation of a Galaxy Cluster**

2.  **Measuring Cosmological Parameters Using Type Ia Supernovae**

## 1. Dynamical Mass Calculation of a Galaxy Cluster

This project focuses on calculating the dynamical mass of a galaxy cluster using spectroscopic redshift data. The core idea is to apply the virial theorem, which relates the kinetic energy of a system (inferred from velocity dispersion) to its gravitational potential energy (related to its mass and size).

### Objectives

* Import and utilize essential Python libraries for scientific computing and data analysis (`numpy`, `matplotlib`, `pandas`, `astropy`).

* Define and apply key astronomical constants.

* Load and preprocess observational data from a CSV file (e.g., `Skyserver_SQL6_17_2025 4_59_10 AM.csv`).

* Clean and aggregate data by calculating the average spectroscopic redshift for unique objects.

* Implement a 3-sigma clipping method to identify and filter out outliers in redshift data, thus defining a galaxy cluster.

* Visualize redshift distributions using box plots.

* Calculate the projected physical diameter of the cluster based on its redshift and the assumed cosmology.

* Determine the velocity dispersion of the cluster members.

* Apply the virial theorem to calculate the dynamical mass of the cluster.

* Convert the calculated mass into solar masses for astronomical context.

### Key Concepts Explored

* **Virial Theorem:** A fundamental theorem in astrophysics used to estimate the mass of self-gravitating systems in dynamical equilibrium.

* **Redshift:** The stretching of light waves as objects move away from the observer, used to determine cosmic distances and velocities.

* **Velocity Dispersion:** A measure of the spread of velocities of galaxies within a cluster, indicating the internal motion and gravitational binding.

* **Distance Modulus:** A measure of cosmic distance based on the difference between apparent and absolute magnitudes of celestial objects.

* **Astropy:** A powerful Python library for astronomy, providing constants, units, and cosmological models.

* **Pandas:** A data manipulation and analysis library, particularly useful for handling tabular data.

### How to Run

1.  **Prerequisites:** Ensure you have Python installed, along with the following libraries:

    ```bash
    pip install numpy matplotlib pandas astropy

    ```

2.  **Data:** Download the `Skyserver_SQL6_17_2025 4_59_10 AM.csv` file (as instructed in the original PDF) and place it in the appropriate directory, or update the `file_path` variable in the notebook.

3.  **Execute:** Open the `1_dynamical_mass.ipynb` notebook in a Jupyter environment (Jupyter Lab, Jupyter Notebook, VS Code with Jupyter extension) and run all cells sequentially.

## 2. Measuring Cosmological Parameters Using Type Ia Supernovae

This project delves into the realm of observational cosmology, using Type Ia Supernovae (SNe Ia) as standard candles to measure the Hubble constant ($H_0$) and estimate the age of the universe. This analysis leverages the Pantheon+SH0ES dataset, a compilation of highly calibrated SNe Ia observations.

### Objectives

* Import and configure necessary Python libraries, including `numpy`, `pandas`, `matplotlib`, `scipy.optimize.curve_fit`, `scipy.integrate.quad`, `astropy.constants`, and `astropy.units`.

* Load and process the Pantheon+SH0ES dataset, extracting Hubble diagram redshift (`zHD`), distance modulus (`MU_SH0ES`), and associated uncertainties (`MU_SH0ES_ERR_DIAG`).

* Plot the Hubble diagram (distance modulus vs. redshift) to visualize the expansion of the universe.

* Fit a cosmological model (e.g., a flat $\Lambda$CDM model) to the supernova data to derive values for the Hubble constant ($H_0$) and the matter density parameter ($\Omega_m$).

* Estimate the age of the universe based on the derived cosmological parameters.

* Analyze the residuals between the observed data and the fitted model to assess the model's accuracy and identify potential systematics.

* Investigate the effect of fixing the matter density parameter ($\Omega_m$) on the derived Hubble constant.

* Compare the results obtained from low-redshift (low-z) and high-redshift (high-z) subsamples of the data.

### Key Concepts Explored

* **Type Ia Supernovae (SNe Ia):** "Standard candles" in cosmology due to their consistent peak luminosity, allowing astronomers to measure cosmic distances.

* **Hubble Diagram:** A plot of distance modulus versus redshift, which illustrates the expansion of the universe.

* **Hubble Constant ($H_0$):** The current rate of expansion of the universe.

* **Distance Modulus ($\mu$):** A logarithmic measure of distance, directly related to the apparent and absolute magnitudes of an object.

* **Cosmological Model (e.g., $\Lambda$CDM):** A theoretical framework describing the composition and evolution of the universe, characterized by parameters like the matter density ($\Omega_m$) and dark energy density ($\Omega_\Lambda$).

* **Redshift (z):** Used to infer the distance and look-back time to distant supernovae.

* **`scipy.optimize.curve_fit`:** A powerful tool for fitting functions to data.

* **`scipy.integrate.quad`:** Used for numerical integration, essential for calculating cosmological distances.

### How to Run

1.  **Prerequisites:** Ensure you have Python installed, along with the following libraries:

    ```bash
    pip install numpy pandas matplotlib scipy astropy

    ```

2.  **Data:** Download the `Pantheon+SH0ES.dat` file from the [Pantheon+ Data Release](https://github.com/PantheonPlusSH0ES/DataRelease/blob/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat) and place it in the same directory as the notebook.

3.  **Execute:** Open the `2_hubble_parameter.ipynb` notebook in a Jupyter environment and run all cells sequentially.

## Repository Structure

![image](https://github.com/user-attachments/assets/39fc8abb-cabd-4ccd-8dd6-f88c731340c6)


## Internship Learnings

These projects provided invaluable hands-on experience in:

* **Astrophysical Data Analysis:** Working with real astronomical datasets and applying statistical methods to extract meaningful insights.

* **Cosmological Modeling:** Understanding and implementing fundamental cosmological equations and models.

* **Python for Science:** Enhancing proficiency in Python's scientific ecosystem, including `numpy`, `pandas`, `matplotlib`, `scipy`, and `astropy`.

* **Problem-Solving:** Developing systematic approaches to analyze complex scientific problems.

* **Scientific Visualization:** Creating informative plots to communicate results effectively.

## Contact

For any questions or further information, please feel free to reach out.

**[Ansh Pradhan]**
[anshpradhan911@gmail.com]
