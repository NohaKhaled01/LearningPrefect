# Event-driven workflows

**The Core Architecture**

- **Event:** A structured message that something happened (e.g., `order.complete`, `s3.object.created`). Can be Prefect-internal or custom/external.
- **Trigger:** The condition that listens for specific events (e.g., `expect={"order.complete"}`).
- **Automation:** The link between a trigger and an action (e.g., "when trigger fires, run this deployment").

**2. How to Create Automations**

- **UI:** Visual builder for triggers and webhooks.
- **Python:** Use `DeploymentEventTrigger` in your deployment code.
- **YAML:** Define triggers in `prefect.yaml` for an IaC approach.
- **API/CLI:** Programmatic creation with `prefect automation create`.

**3. Common Use Cases**

- **Chaining Flows:** Run a downstream flow after an upstream flow completes.
- **Webhooks:** Trigger flows from external systems via a unique URL.
- **S3 File Processing:** Run a flow when a file lands in a bucket.
- **Debouncing:** Handle bursts of events with a single flow run.

**4. Key Considerations**

- **Event Emission:** Something must emit the event to Prefect. Prefect flows do this automatically. For external systems, you need to configure a bridge (e.g., AWS Lambda, Kafka Connect).
- **Event vs. Schedule:** Use events for real-time, resource-efficient workflows. Use schedules for predictable, guaranteed execution windows.

[Full Explanation - Not Summary](<./Event driven workflows Full Explanation - Not Summary.md>)