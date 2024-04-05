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
        total_footprint, energy_emissions, material_emissions, waste_emissions, shipping_emissions = kalkulator.calculate_manufacturing_footprint() # calc.calculate_manufacturing_footprint()
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
