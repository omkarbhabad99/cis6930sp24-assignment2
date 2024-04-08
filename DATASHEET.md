# 1. Introduction

The aim of this project is to focus on enhancing data from public police records. The first step involved extracting data from PDF files found on a police department’s website, followed by augmenting this data with additional information. This data augmentation process included details such as weather conditions at the time of incidents, ranking locations of incidents by their frequency, and categorizing incidents by type. These enhancements aimed to increase the value of the data for further analysis, with a careful consideration for fairness and avoiding bias.

Along with the technical efforts, this datasheet for the dataset was created. The datasheet provides clear information on the data’s origin, its contents, and guidelines for its use, ensuring transparency and responsibility in data handling. This project showcases the ability to not only manipulate and enrich data but also to approach data use with a commitment to fairness and ethical standards, particularly when dealing with sensitive information like police records.

## 1.1 Objectives

For those who will utilize this enriched dataset, the project aims to provide them with a detailed and transparent overview of the data through the creation of a datasheet. This datasheet is intended to offer users essential insights into the data's origin, its characteristics, and its appropriate uses, helping to prevent misuse and aiding in the selection of data that best fits their specific needs. By doing so, the project supports not just the immediate users but also contributes to the broader community involved in data-driven decision-making, including policymakers, journalists, and researchers. This approach ensures that the dataset can be used responsibly and ethically, facilitating better outcomes from the analysis derived from this data.

Moreover, this project acknowledges the diverse needs and contexts in which this dataset might be used. Therefore, while providing a set of guiding principles and information through the datasheet, it also allows for flexibility in its application across various domains and organizational requirements. This flexibility ensures that the datasheet remains relevant and beneficial across different use cases. Through this project, the intention is to foster a culture of reflection and responsibility among dataset creators and users, encouraging a more thoughtful and ethical approach to data handling and utilization in the realm of public safety and beyond.

# 2. Development Process

The development of this project was a step-by-step journey that started with the extraction of police department data from PDFs, an initiative building on the foundation laid by a previous assignment. The goal was to not only extract this data but to significantly enrich it with additional context such as weather conditions during incidents and geographical insights indicating the incident locations. This data augmentation aimed to make the dataset more insightful and applicable for varied analytical purposes.

The process involved utilizing APIs for weather data and geographical calculations to ascertain precise incident locations. A structured SQLite database was set up to systematically manage the extracted and augmented data, facilitating efficient data manipulation for analysis and reporting. Key components like the `assignment2.py` script underwent several iterations to hone its functionality in data processing. Challenges such as inconsistencies of API responses and managing the speed of program using multithreading were systematically addressed through rigorous testing and adjustments.

This streamlined development process, from meticulous data extraction to the careful crafting of a comprehensive datasheet, reflects a thoughtful approach aimed at delivering an enhanced, well-documented dataset for public safety data analysis.

# 3. Questions and Workflow

## 3.1 Motivation

### Purpose of Creation:
The dataset was created as a part of coursework to develop a model that automates the process of extracting and analyzing incident report data from the Norman Police Department's publicly available PDF documents. It was mainly devided into two parts, 1. Data Extraction Part and 2. Data Augmentation Part. The main goal  was to bridge a specific gap in data accessibility, transforming unstructured data into a structured format that allows for efficient querying and analysis. This process is particularly aimed at enhancing the ability of researchers, policymakers, and the public to engage in data-driven discussions about public safety.

### Creators
The dataset was developed by me (Omkar Sunil Bhabad) a student of Data Engineering course at the University of Florida, under the guidance of the Professor Christan Grant. 

### Funding
This project was developed as part of  data engineering coursework at the University of Florida. It did not receive direct funding from external sources. However, to support the project, especially for tasks requiring cloud services, the Professor Grant allocated Google Cloud credits to students. These credits were used primarily for accessing APIs necessary for data augmentation, such as weather information retrieval and geocoding services. 

## 3.2 Composition

### Instances Representation
The dataset consists of augmented instances derived from police incident reports from the Norman Police Department. Initially presented in PDF format, these reports undergo a transformation process, culminating in a structured and enriched dataset housed within a SQLite database. The augmentation process enriches each instance with additional layers of contextual information, extending beyond basic details to include enhanced elements such as the day of the week, time of day, prevailing weather conditions at the incident's location, location rank based on incident frequency, the side of town determined through geocoding, incident nature rank, and the EMSSTAT status.

### Quantity of Instances
The dataset's size fluctuates depending how many daily instances files you feed to your program. Generally a single file will have 300-350 incidents in it. So an entire months data can go up to 10000 Instances. 

### Completeness of the Dataset
The dataset represents a comprehensive extraction of available incident PDF reports from the Norman Police Department's website. It is not a sample but a complete set of all available instances during the specific time frames chosen for analysis. The dataset aims to provide exhaustive coverage of the reported incidents within the given periods.

### Data Composition
Each instance in the dataset consists of structured data derived from the "raw" text within the PDF reports. This structured data encompasses:
- `Day of the Week`: Calculated from the incident time, representing the day of the week on which the incident occurred, enhancing temporal analysis capabilities.
- `Time of Day`: Extracted from the incident time, indicating the specific hour of the day the incident was reported, allowing for pattern analysis across different times.
- `Weather Conditions`: Augmented information detailing the weather at the time and location of the incident, providing context for environmental conditions possibly influencing or related to the incident.
- `Location Rank`: A rank assigned to the location based on the frequency of incidents reported at that location, offering insights into high-risk areas.
- `Side of Town`: Determined through geocoding techniques, this element categorizes the incident location into one of eight predefined sectors (N, S, E, W, NW, NE, SW, SE), enriching the geographical analysis.
- `Incident Rank`: A rank assigned based on the frequency of the incident nature, facilitating the identification of common incident types.
- `Nature of the Incident`: A descriptive categorization of the incident, retained from the original report, crucial for content analysis.
- `EMSSTAT`: A boolean value indicating whether the incident was tagged with an EMSSTAT status, highlighting incidents involving emergency medical services.

### Labels and Targets
Each instance does not have a specific label or target in the traditional sense used in supervised machine learning tasks. However, the nature of the incident could be utilized as a categorical label for classification or analysis purposes.

### Missing Information
There are some data entries where information is missing but is it very rate. However, limitations may arise from the formatting chage in PDF reports, since the extraction depends on physical layout of the pdf. 

### Relationships Between Instances
The dataset primarily comprises discrete incident reports and does not explicitly encode relationships between individual instances, such as social network links or user interactions. Unless in few cases like if address of two incidents are same and one of them is EMSSTAT then both are considered to be EMSSTAT. Other than this each incident stands as an independent entry without direct connections to others within the dataset.

### Errors, Noise, and Redundancies
Given the automated process of extracting data from PDFs, there might be minor errors or noise, such as missing data or unable to fetch older PDFs. 

### External Resources and Self-Containment
The development of this dataset involved using external resources like the fetching data from Norman Police department's website, Open-Meteo API for weather data and Google Maps for geocoding. Despite this, the dataset is designed to be self-contained, allowing for comprehensive analysis with the enriched data it provides. 

### Confidentiality and Privacy
The dataset consists of publicly available incident reports released by the Norman Police Department. It does not contain confidential information, as all data is derived from documents intended for public release. Any potentially sensitive information is already redacted by the issuing authority before the dataset's creation.

### Potentially Offensive Content
While the dataset itself is neutral, containing structured information about police incidents, the nature of some incidents (e.g., crimes) described in the data could be distressing or sensitive to some users. The dataset is intended for informational and analytical purposes, with an emphasis on public safety and research.

### Subpopulations Identification
The dataset does not specifically identify subpopulations by age, gender, or other demographic characteristics. The incidents are reported with a focus on the events rather than the individuals involved, maintaining a neutral stance on demographic categorization. Consequently, no distributions regarding subpopulations are available within the dataset.

### Individual Identification
Given the nature of the data, direct or indirect identification of individuals is highly unlikely. The dataset comprises aggregated incident reports that focus on the incidents themselves rather than personal details. Any potentially identifying information is either generalized or redacted prior to publication by the Norman Police Department, ensuring privacy and confidentiality.


## 3.3 Collection Process

### Data Acquisition
The data associated with each incident was directly observable and extracted from publicly available PDF reports published by the Norman Police Department. These reports include raw text detailing incidents that occurred within a specified timeframe, including the date, time, location, nature, and incident number of each event.

### Collection Mechanisms
The collection process employed software programs developed in Python, utilizing libraries such as `fitz` (PyMuPDF) for PDF parsing, `sqlite3` for database management, and `urllib` for downloading PDF files from specified URLs. The validity of these software tools and libraries is well-established in the developer and research communities, ensuring reliable data extraction and storage.

### Data Collection Personnel
The data collection and processing were automated through software scripts without direct human involvement in the data entry process, minimizing the potential for human error and bias. The automation of data collection was managed by me, a team of computer science student as part of an academic project, focusing on the application of data engineering principles.

### Ethical Review Processes
The ethical review process for this project, focusing on data from police incident reports, emphasized data privacy, adherence to laws regarding public data use, and efforts to mitigate bias. It ensured compliance with the University of Florida's research guidelines and highlighted transparency and accountability in data handling. This review aimed to responsibly manage sensitive information while maintaining high ethical standards in data collection and augmentation, ensuring the project aligns with best practices in privacy, fairness, and academic integrity.

### Notification and Consent
Given that the data was sourced from publicly available reports, individual notifications about the collection were not applicable. The Norman Police Department publishes these reports as a part of its commitment to transparency and public safety, implicitly allowing for the public dissemination and analysis of the data contained within.

### Consent Mechanism
As the data was extracted from publicly available sources published by a government entity, the issue of individual consent for data collection and usage does not directly apply. The reports are intended for public use, and there is no mechanism for individuals to revoke consent as the information is a matter of public record.

### Impact Analysis
An explicit analysis of the potential impact of the dataset and its use on individuals (such as a data protection impact analysis) has not been conducted within the scope of this project. The project's focus is on public data intended for analysis and research purposes, emphasizing incidents rather than personal data. However, care was taken to ensure that the dataset does not include personally identifiable information beyond what is made publicly available by the Norman Police Department.

## 3.4 Preprocessing/Cleaning/Labeling

### Preprocessing Details
Yes, preprocessing and cleaning of the data were undertaken to transform the "raw" PDF reports from the Norman Police Department into a structured format suitable for analysis and storage within a SQLite database. The specific steps included:

- **PDF Parsing**: The PDF documents were parsed to extract text content, including incident times, numbers, locations, natures, and ORIs.
- **Data Extraction**: Text extracted from PDFs was processed to identify and separate different pieces of information relevant to each incident report.
- **Labeling**: No additional labeling was performed beyond the categorization inherent in the data provided by the Norman Police Department.

### Raw Data Preservation
The "raw" PDF reports are publicly available via the Norman Police Department's website. The project did not store a separate copy of these PDFs beyond what was necessary for processing. Users interested in the "raw" data can access it directly from the official source.

### Preprocessing Software Availability
The preprocessing was performed using custom Python scripts leveraging libraries such as PyMuPDF (fitz) for PDF parsing. While the specific preprocessing scripts used in this project are bundled with the project repository, they are designed to operate on the PDF reports available from the Norman Police Department. 

## 3.5 Uses

### Current Uses of the Dataset
The dataset is currently being used in academic research to analyze public safety trends, with a focus on identifying patterns in incident types, times, and locations. It serves as a valuable resource for studies on the impact of environmental factors, like weather conditions, on incident rates. Additionally, the dataset is utilized in data engineering courses to teach students about data collection, processing, augmentaton and analysis techniques. Its comprehensive nature allows for a wide range of analyses, from temporal and geographical patterns to the exploration of emergency response statistics, making it a versatile tool for enhancing public safety strategies and informing policy decisions.

### Potential Tasks
This dataset could be valuable for a variety of tasks beyond the educational scope, including but not limited to:
- Crime pattern analysis over time and location.
- Predictive modeling to forecast crime trends or identify high-risk areas.
- Sociological studies examining the nature of incidents reported to police.
- Development of data visualization tools for public safety awareness.

### Impact on Future Uses
While the dataset provides a structured format for analyzing police incident reports, users should exercise caution when interpreting the data, especially regarding:
- Potential biases inherent in the data due to the nature of law enforcement reporting and activity.
- Privacy concerns, ensuring that no personal information is used in a manner that could harm individuals.
- The context of data collection, understanding that it reflects incidents reported to or observed by the police, which may not represent all crime occurrences.

To mitigate these risks, dataset consumers are encouraged to:
- Apply ethical considerations and privacy-preserving techniques when analyzing and presenting data.
- Critically assess and contextualize findings, especially when drawing conclusions about crime rates or public safety.

### Inappropriate Uses
The dataset should not be used for:
- Identifying or targeting specific individuals or groups.
- Making or supporting legal decisions or actions.
- Any application where the lack of representativeness or potential biases could lead to unfair or harmful outcomes.

## 3.6 Distribution

### Distribution Method
The dataset will be made available via a GitHub repository (which is private for now but possibly will be open for future use), which provides a convenient platform for distribution, version control, and collaboration. While the dataset itself does not have a Digital Object Identifier (DOI) at this time, the GitHub repository URL serves as an accessible distribution point.

### Regulatory Restrictions
No known export controls or other regulatory restrictions apply specifically to the dataset. Users are responsible for ensuring that their use of the dataset complies with all applicable laws and regulations.

## 3.7 Maintenance

### Support/Hosting/Maintenance
The dataset will be maintained by the original creator (Omkar Sunil Bhabad) and hosted on GitHub, providing a centralized platform for access, version control, and updates. This approach ensures that the dataset remains accessible and up-to-date for all users.

### Contact Information
For any inquiries, issues, or suggestions related to the dataset, users can contact the maintainer via the project's GitHub Issues page or directly through email at [omkarbhabad99@gmail.com]. 


### Contributions to the Dataset
Contributions to extend, augment, or improve the dataset are welcome and can be made through GitHub Pull Requests. 
Instructiona to run the program are given in README.md file.

## 4. Impact and Challenges

This academic project, centered around enhancing and analyzing police incident report data, contributes to the broader movement towards transparency and accountability in data-driven research and application.

### Adoption and Initial Successes
- **Academic Utility**:The dataset, complemented by a detailed datasheet, has become an educational tool in data engineering and computer science disciplines, enabling students to understand the intricacies of data collection, augmentation, and ethical considerations.
- **Research Application**: It's leveraged in academic research to explore public safety trends, offering insights into how environmental and temporal factors influence incident rates. This aligns with the initiative of using datasheets to clarify data provenance and usage, fostering a deeper understanding of the dataset’s scope and limitations.

### Implementation Challenges
- **Scope of Documentation**: Given the project's academic nature, the datasheet primarily focuses on technical and ethical considerations relevant to the dataset's content and use. The challenge lies in ensuring that this documentation remains accessible and informative for all potential users, including those outside the immediate academic circle.
- **Bias and Privacy**: Addressing biases and privacy concerns within the dataset has been a priority, though the datasheet format primarily prompts reflection and disclosure rather than providing direct solutions to these complex issues.

### The Path Forward
## 4. Impact and Challenges

The project's integration of datasheets for its dataset aligns with the growing trend towards enhancing transparency and accountability in data handling, particularly in academic settings. While this initiative is primarily educational, it mirrors broader efforts in the tech industry and academia to document datasets comprehensively.

### Adoption and Initial Successes
- **Academic Emphasis**: This project, rooted in an academic environment, highlights the importance of detailed documentation in research and education. By incorporating a datasheet, it serves as an example for students and researchers on how to approach data analysis with an emphasis on transparency and ethical considerations.

### Implementation Challenges
- **Educational Context Limitations**: In the academic setting of this project, certain challenges such as adapting datasheets to specific research needs or the dynamic nature of datasets are less prominent. However, the project does face educational challenges, such as ensuring that students understand the importance and know-how of creating and updating datasheets.
- **Addressing Biases**: While the project aims to minimize biases through its collection and augmentation process, the educational context provides a unique opportunity to discuss and explore the complexities of biases in datasets and the limitations of datasheets in fully addressing these issues.

### Collaboration and Learning
- The project encourages collaboration among students from various disciplines, providing a learning opportunity to tackle ethical considerations and biases in data collection and analysis. It serves as a practical exercise in applying theoretical knowledge to real-world data.

### Organizational Impact
- Within the academic framework, the project necessitates a slight shift in how data-related projects are approached, emphasizing the need for detailed documentation and ethical considerations from the outset.

### The Path Forward
Despite the project's scale and scope being primarily educational, it underscores the value of datasheets in promoting a thoughtful, transparent, and accountable approach to data analysis. This initiative not only benefits the students involved by instilling best practices in data handling but also contributes to the broader conversation on responsible AI development and deployment. The experience gained from this project can inspire similar approaches in other academic and research endeavors, reinforcing the importance of datasheets in enhancing the integrity of data-driven projects.

