import os
from jinja2 import Environment, FileSystemLoader



class IaCGenerator:
    """
    Reads a mapped_spec dict and generates Terraform .tf files
    using Jinja2 templates, one file per node plus a provider.tf.
    """

    def __init__(self, templates_root="stage3_iac/templates"):
        self.templates_root = templates_root

    def generate(self, mapped_spec, output_directory):
        provider = mapped_spec.get("provider")
        region = mapped_spec.get("region")
        nodes = mapped_spec.get("nodes", [])

        if provider not in ("aws", "azure"):
            print(f"[IaCGenerator] ERROR: Unsupported provider '{provider}'")
            return False

        print(f"[IaCGenerator] Starting generation for provider='{provider}', region='{region}'")

        # Step 1: create output directory if it doesn't exist
        try:
            os.makedirs(output_directory, exist_ok=True)
            print(f"[IaCGenerator] Ensured output directory exists: {output_directory}")
        except OSError as e:
            print(f"[IaCGenerator] ERROR: Could not create output directory: {e}")
            return False

        # Step 2: set up Jinja2 environment for this provider's template folder
        provider_templates_dir = os.path.join(self.templates_root, provider)
        if not os.path.isdir(provider_templates_dir):
            print(f"[IaCGenerator] ERROR: Template folder not found: {provider_templates_dir}")
            return False

        env = Environment(loader=FileSystemLoader(provider_templates_dir))

        # Step 3: generate provider.tf
        try:
            provider_template = env.get_template("provider.tf.j2")
            provider_content = provider_template.render(region=region)
            provider_path = os.path.join(output_directory, "provider.tf")
            with open(provider_path, "w") as f:
                f.write(provider_content)
            print(f"[IaCGenerator] Generated provider.tf -> {provider_path}")
        except Exception as e:
            print(f"[IaCGenerator] ERROR: Failed to generate provider.tf: {e}")
            return False

        # Step 4: generate one .tf file per node
        for node in nodes:
            node_id = node.get("id")
            category = node.get("category")
            node_type = node.get("type")
            config = node.get("config", {})

            template_filename = f"{node_type}.tf.j2"
            print(f"[IaCGenerator] Processing node '{node_id}' (type={node_type}, category={category})")

            try:
                node_template = env.get_template(template_filename)
            except Exception as e:
                print(f"[IaCGenerator] ERROR: Template not found for type '{node_type}': {e}")
                return False

            try:
                render_vars = {
                    "node_id": node_id,
                    "config": config,
                    "category": category,
                }

                # Azure VM template needs to know which node is the network,
                # since it can't be hardcoded to a specific node id.
                if node_type == "azurerm_virtual_machine":
                    network_node = next(
                        (n for n in nodes if n.get("type") == "azurerm_virtual_network"),
                        None
                    )
                    if network_node is None:
                        print(f"[IaCGenerator] ERROR: VM node '{node_id}' requires a virtual network node, none found")
                        return False
                    render_vars["network_node_id"] = network_node["id"]

                node_content = node_template.render(**render_vars)
                node_path = os.path.join(output_directory, f"{node_id}.tf")
                with open(node_path, "w") as f:
                    f.write(node_content)
                print(f"[IaCGenerator] Generated {node_id}.tf -> {node_path}")
            except Exception as e:
                print(f"[IaCGenerator] ERROR: Failed to render/write node '{node_id}': {e}")
                return False

        print(f"[IaCGenerator] Generation complete. {len(nodes)} node file(s) + provider.tf written.")
        return True