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
* Select modeling techniques: Determine which algorithms to try (with scikit-learn Library and tensorflow Library).
  - 1-Supervised Learning
      + LSTM (Common Tasks: Sequence classification, regression)
  - 2- Unsupervised Learning
  - 3- Semi-Supervised Learning
  - 4- Self-Supervised Learning
  - 5- Reinforcement Learning
 
	



* Generate test design: Pending your modeling approach, you might need to split the data into training, test, and validation sets.
* Build model: As glamorous as this might sound, this might just be executing a few lines of code like “reg = LinearRegression().fit(X, y)”.
* Assess model: Generally, multiple models are competing against each other, and the data scientist needs to interpret the model results based on domain knowledge, the pre-defined success criteria, and the test design.

###	VI. Deployment
* Evaluate results: Do the models meet the business success criteria? Which one(s) should we approve for the business?
* Review process: Review the work accomplished. Was anything overlooked? Were all steps properly executed? Summarize findings and correct anything if needed.
* Determine next steps: Based on the previous three tasks, determine whether to proceed to deployment, iterate further, or initiate new projects.








---------------------------------------------------
## Main Learning Methods in Deep Learning

Deep learning primarily employs three main learning paradigms, each suited to different types of data and tasks:

---

### 1. **Supervised Learning**
- **Description:**  
  The model learns from labeled data, where each input is paired with a known output (label). The goal is to learn a mapping from inputs to outputs to predict labels on new, unseen data.  
- **Common Tasks:** Classification, regression  
- **Example Models:**  
  - Convolutional Neural Networks (CNNs) for image classification  
  - Recurrent Neural Networks (RNNs) and Long Short-Term Memory networks (LSTMs) for sequence data  
  - Deep Belief Networks (DBNs) with fine-tuning via backpropagation  
- **Applications:** Image recognition, speech recognition, natural language processing, medical diagnosis

---

### 2. **Unsupervised Learning**
- **Description:**  
  The model learns patterns from unlabeled data without explicit output labels. It discovers the underlying structure or distribution of the data.  
- **Common Tasks:** Clustering, dimensionality reduction, feature learning, generative modeling  
- **Example Models:**  
  - Autoencoders and Variational Autoencoders (VAEs) for representation learning and clustering  
  - Deep Belief Networks (DBNs) for feature extraction  
  - Generative Adversarial Networks (GANs) for data generation  
- **Applications:** Customer segmentation, anomaly detection, data compression, image generation

---

### 3. **Reinforcement Learning (Deep Reinforcement Learning)**
- **Description:**  
  An agent learns to make sequential decisions by interacting with an environment, receiving rewards or penalties, and optimizing its policy to maximize cumulative reward. Deep learning models approximate value functions or policies.  
- **Example Models:**  
  - Deep Q-Networks (DQNs) combining Q-learning with deep neural networks  
  - Actor-Critic methods  
  - Policy Gradient methods  
- **Applications:** Robotics, autonomous driving, game playing (e.g., AlphaGo), recommendation systems

---

![image](https://github.com/user-attachments/assets/501bb935-6217-4fda-aaab-111a351e50a9)


-----------------------------------------------------------------------------------------------------------------
### Main Tasks in Deep Learning
![image](https://github.com/user-attachments/assets/a16ab370-36b6-4ef3-8bad-8ce723667b66)

![image](https://github.com/user-attachments/assets/ba533cb9-66f2-40a0-88af-72fee3e2c7a5)
