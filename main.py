from dotenv import load_dotenv
from mira_sdk import MiraClient, Flow
from mira_sdk.exceptions import FlowError
import os
import glob

# Load environment variables from the .env file
load_dotenv()

# Initialize the MIRA client with the API key
client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})

# Function to deploy the flow
def deploy_flows():
    # Path to the YAML file (recipe-generator.yaml)
    flow_file = "flows/recipe-generator.yaml"

    try:
        # Create flow from the YAML file
        flow = Flow(source=flow_file)

        # Deploy the flow to the platform
        client.flow.deploy(flow)

        # Get flow name from the filename and construct flow ID
        flow_name = os.path.splitext(os.path.basename(flow_file))[0]
        flow_id = f"akshitadimpu/{flow_name}"  # Ensure this is the correct flow ID

        # Construct the Flow URL
        flow_url = f"https://mira.network/flows/akshitadimpu/{flow_name}"

        print(f"Flow deployed successfully with ID: {flow_id}")
        print(f"Flow URL: {flow_url}")  # Output the flow URL

    except FlowError as e:
        print(f"Error deploying flow {flow_file}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error with {flow_file}: {str(e)}")

# Function to execute the deployed flow
def test_flow(flow_id, inputs):
    try:
        # Execute the flow with provided inputs
        result = client.flow.execute(flow_id, inputs)
        return result
    except FlowError as e:
        print(f"Error running flow: {str(e)}")
        return None

# Main function
def main():
    # Deploy the flow
    print("Deploying flow...")
    deploy_flows()

    # Sample input for testing the recipe generator flow
    ingredients = "chicken, garlic, onion, tomato, olive oil"
    cuisine = "Italian"
    dietary_restrictions = "gluten-free"

    # Execute the recipe generator flow with the sample input
    print("\nTesting recipe-generator flow...")
    result = test_flow("akshitadimpu/recipe-generator", {
        "ingredients": ingredients,
        "cuisine": cuisine,
        "dietary_restrictions": dietary_restrictions
    })

    # Output the result of the recipe
    if result:
        print("\nGenerated Recipe:")
        print(result)

if __name__ == "__main__":
    main()
