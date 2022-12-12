# Prefect_Test
 Testing Prefect Workflow Orchestration

## Login to Prefect Cloud

https://orion-docs.prefect.io/ui/cloud-getting-started/#configure-a-local-execution-environment

```
$ prefect cloud login -k xxx_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

```

### Create a FLow

You can have **tasks** and **flows**, you have to have at least one **flow**.  You call a **task** from a **flow**.

```
@task
def call_api(url):
    response = requests.get(url)
    print(response.status_code)
    return response.json()

@flow
def api_flow(url):
    fact_json = call_api(url)
    return fact_json
```

## Deployments

[https://docs.prefect.io/tutorials/deployments/](https://docs.prefect.io/tutorials/deployments/)

```
$ prefect deployment build ./log_flow.py:log_flow -n log-simple -q test
```

* `prefect deployment build` is the Prefect CLI command that enables you to prepare the settings for a deployment.
* `./log_flow.py:log_flow` specifies the location of the flow script file and the name of the entrypoint flow function, separated by a colon.
* `-n` log-simple specifies a name for the deployment.
* `-q` test specifies a work queue for the deployment. Work queues direct scheduled runs to agents.

Entrypoint Function

```
if __name__ == "__main__":
    name = sys.argv[1]
    log_flow(name)
```

### Apply the Deployment

```
prefect deployment apply log_flow-deployment.yaml
```

### Run the Deployment

```
prefect deployment run 'log-flow/log-simple'
```

### Monitor with an Agent

```
prefect agent start -q test
```

* We specified the `test` work queue when creating the deployment.
* The agent is configured to pick up work from the `test` work queue, so it will execute flow runs from the `log-flow/log-simple` deployment (and any others that also point at this queue).


