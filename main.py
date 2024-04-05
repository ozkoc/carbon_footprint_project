import matplotlib.pyplot as plt  # for creating the pie chart of emissions categories.
from matplotlib.backends.backend_pdf import PdfPages # for creating a PDF file to save the plot in it.
from reportlab.lib.pagesizes import letter  # for setting the page size of the PDF report.
from reportlab.pdfgen import canvas  # for creating the PDF report.
from PyPDF2 import PdfMerger  # for merging the pie chart and report PDFs into a single PDF.

import calculator as calc


def main():
    """The main function runs the carbon footprint calculation, generates the report,
    and creates a merged PDF containing the pie chart and report.
    """
    try:
        kalkulator = calc.Calculator()   
        
        # Run the carbon footprint calculation and report generation
        client_name = str(input("Enter the company's name:> \n"))    
        total_footprint, energy_emissions, material_emissions, waste_emissions, shipping_emissions = kalkulator.calculate_manufacturing_footprint() # call the class kalkulator and function calculate_manufacturing_footprint() in it.
        categories = ['Energy', 'Material', 'Waste', 'Shipping']
        emissions = [energy_emissions, material_emissions, waste_emissions, shipping_emissions]
        # merge pie chart and report page together in asingle pdf
        merger = PdfMerger()
        merger.append(calc.save_pie_chart_as_pdf(emissions, categories, filename='Pie_emissions.pdf'))
        merger.append(calc.generate_report(total_footprint, energy_emissions, material_emissions, waste_emissions, shipping_emissions,
                    company_name=client_name))

        merger.write('Merged_Report.pdf')
        print(merger)
        merger.close()

    except ValueError:
        print("Invalid input. Please enter numerical values.")


# Run the main function
if __name__ == "__main__":
    main()
