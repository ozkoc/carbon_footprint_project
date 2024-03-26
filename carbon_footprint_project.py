import datetime  # for accessing the current date and time.
import matplotlib.pyplot as plt  # for creating the pie chart of emissions categories.
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter  # for setting the page size of the PDF report.
from reportlab.pdfgen import canvas  # for creating the PDF report.
from PyPDF2 import PdfMerger  # for merging the pie chart and report PDFs into a single PDF.

# Constants for emission factors
ENERGY_EMISSION_FACTOR = 0.0002  # in tons of CO2 per kWh
MATERIAL_EMISSION_FACTOR = 0.001  # in tons of CO2 per pound of material
WASTE_EMISSION_FACTOR = 0.004  # in tons of CO2 per pound of waste
SHIPPING_EMISSION_FACTOR = 0.0001  # in tons of CO2 per mile shipped


def calculate_manufacturing_footprint():
    """The calculate_manufacturing_footprint function calculates the total carbon footprint based on user inputs and
    returns the total footprint along with energy, material, waste, and shipping emissions of a manufacturing company.

    Returns:
       Total_footprint and each emission
    """

    # Prompt user for input

    energy_consumption = float(input("Enter energy consumption in kWh: "))
    material_used = float(input("Enter weight of material used in kgs: "))
    waste_produced = float(input("Enter waste produced in kgs: "))
    distance_shipped = float(input("Enter distance shipped in kms: "))

    # Calculate emissions
    energy_emissions = energy_consumption * ENERGY_EMISSION_FACTOR
    material_emissions = material_used * MATERIAL_EMISSION_FACTOR
    waste_emissions = waste_produced * WASTE_EMISSION_FACTOR
    shipping_emissions = distance_shipped * SHIPPING_EMISSION_FACTOR

    # Total carbon footprint
    total_footprint = energy_emissions + material_emissions + waste_emissions + shipping_emissions
    return total_footprint, energy_emissions, material_emissions, waste_emissions, shipping_emissions


def suggest_improvements(energy_emissions, material_emissions, waste_emissions, shipping_emissions):
    """ The suggest_improvements function suggests improvements based on emissions data,
    such as switching to renewable energy, evaluating material usage,
    improving waste management strategies, and optimizing logistics.
    """

    suggestions = []
    # Suggest improvements based on emissions data
    if energy_emissions > 1:
        suggestions.append("- Consider switching to renewable energy sources such as solar or wind power.")
    if material_emissions > 1:
        suggestions.append("- Evaluate material usage and explore recycling or sustainable materials.")
    if waste_emissions > 1:
        suggestions.append("- Improve waste management strategies to reduce emissions from waste.")
    if shipping_emissions > 1:
        suggestions.append("- Optimize logistics to reduce emissions from shipping.")

    # Additional generic suggestions
    suggestions.append("- Regularly maintain equipment to ensure energy efficiency.")
    suggestions.append("- Train staff on sustainability practices to foster an eco-friendly workplace culture.")

    return '\n'.join(suggestions)


def save_pie_chart_as_pdf(emissions, categories, filename):
    """The save_pie_chart_as_pdf function creates a pie chart representing the emissions categories,
    saves the chart as an image within the current directory, and appends the image to a new PDF file.

    Args:
        emissions (int): emissions values
        categories (str): categories for emissions
        filename (obj): pie chart

    Returns:
        _pdf file
    """

    # Create a figure with a larger size for better viewing experience
    plt.figure(figsize=(10, 6))

    # Create a pie chart
    plt.pie(emissions, labels=categories, autopct='%1.1f%%', startangle=140,
            wedgeprops={"linewidth": 1, "edgecolor": "white"})

    # Add a legend
    plt.legend(labels=categories, loc='upper right', title='Emissions Categories')

    plt.title('Carbon Emissions Rates in the Company', fontsize=24)

    # Save the pie chart to a PDF
    with PdfPages(filename) as pdf:
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

    return filename


def generate_report(total_footprint, energy_emissions, material_emissions, waste_emissions, shipping_emissions,
                    company_name):
    """The generate_report function creates a PDF report
    that includes emissions data and suggestions for reduction."""

    # Data for plotting
    categories = ['Energy', 'Material', 'Waste', 'Shipping']
    emissions = [energy_emissions, material_emissions, waste_emissions, shipping_emissions]

    # Create a PDF report
    pdf_filename = 'Numbers_Suggestions.pdf'
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf.setTitle('Emission Numbers and Suggestions')

    # Generate the report text
    text = pdf.beginText(40, 750)
    text.setFont("Helvetica", 12)
    report = f"""
    Carbon Footprint Report

    Client: {company_name}

    Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    -------------------------------------------------------------
    *Energy Emissions: {energy_emissions:.2f} tons of CO2

    *Material Emissions: {material_emissions:.2f} tons of CO2

    *Waste Emissions: {waste_emissions:.2f} tons of CO2

    *Shipping Emissions: {shipping_emissions:.2f} tons of CO2

    ***Total Carbon Footprint: {total_footprint:.2f} tons of CO2
    -------------------------------------------------------------
    Suggestions for Reduction:
    {suggest_improvements(energy_emissions, material_emissions, waste_emissions, shipping_emissions)}

    For a detailed analysis and customized reduction strategies, please consult with our sustainability experts.
    """
    text.textLines(report)
    pdf.drawText(text)

    # Save PDF
    pdf.save()

    return pdf_filename


def main():
    """The main function runs the carbon footprint calculation, generates the report,
    and creates a merged PDF containing the pie chart and report.
    """
    try:
        # Run the carbon footprint calculation and report generation

        total_footprint, energy_emissions, material_emissions, waste_emissions, shipping_emissions = calculate_manufacturing_footprint()
        categories = ['Energy', 'Material', 'Waste', 'Shipping']
        emissions = [energy_emissions, material_emissions, waste_emissions, shipping_emissions]
        # merge pie chart and report page together in asingle pdf
        merger = PdfMerger()
        merger.append(save_pie_chart_as_pdf(emissions, categories, filename='Pie_chart_for_emissions_rates.pdf'))
        merger.append(
            generate_report(total_footprint, energy_emissions, material_emissions, waste_emissions, shipping_emissions,
                            company_name="Client A"))

        merger.write('Merged_Report.pdf')
        print(merger)
        merger.close()

    except ValueError:
        print("Invalid input. Please enter numerical values.")


# Run the main function
if __name__ == "__main__":
    main()
