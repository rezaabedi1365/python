- https://www.datascience-pm.com/crisp-dm-2/

# CRISP
![image](https://github.com/user-attachments/assets/9e743a10-2a34-48ec-a596-05aef0cdbd0c)

###	I. Business Understanding
* Determine business objectives:
  	- You should first “thoroughly understand, from a business perspective, what the customer really wants to accomplish.” (CRISP-DM Guide) and then define business success criteria.
* Assess situation:
  	- Determine resources availability, project requirements, assess risks and contingencies, and conduct a cost-benefit analysis.
* Determine data mining goals:
	- In addition to defining the business objectives, you should also define what success looks like from a technical data mining perspective.
* Produce project plan:
  	- Select technologies and tools and define detailed plans for each project phase.
  
###	II. Data Understanding
* Collect initial data: Acquire the necessary data and (if necessary) load it into your analysis tool.
* Describe data: Examine the data and document its surface properties like data format, number of records, or field identities.
* Explore data: Dig deeper into the data. Query it, visualize it, and identify relationships among the data.
* Verify data quality: How clean/dirty is the data? Document any quality issues.		


###	III. Data Preparation (پالایش دیتای خام)
* Select data: Determine which data sets will be used and document reasons for inclusion/exclusion.
* Clean data: Often this is the lengthiest task. Without it, you’ll likely fall victim to garbage-in, garbage-out. A common practice during this task is to correct, impute, or remove erroneous values.
* Construct data: Derive new attributes that will be helpful. For example, derive someone’s body mass index from height and weight fields.
* Integrate data: Create new data sets by combining data from multiple sources.
* Format data: Re-format data as necessary. For example, you might convert string values that store numbers to numeric values so that you can perform mathematical operations.
		
###	IV. Modeling
* Select modeling techniques: Determine which algorithms to try (e.g. regression, neural net).
* Generate test design: Pending your modeling approach, you might need to split the data into training, test, and validation sets.
* Build model: As glamorous as this might sound, this might just be executing a few lines of code like “reg = LinearRegression().fit(X, y)”.
* Assess model: Generally, multiple models are competing against each other, and the data scientist needs to interpret the model results based on domain knowledge, the pre-defined success criteria, and the test design.
###	VI. Deployment
* Evaluate results: Do the models meet the business success criteria? Which one(s) should we approve for the business?
* Review process: Review the work accomplished. Was anything overlooked? Were all steps properly executed? Summarize findings and correct anything if needed.
* Determine next steps: Based on the previous three tasks, determine whether to proceed to deployment, iterate further, or initiate new projects.


