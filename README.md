# k8s-kapitan-fluxcd-example


## Setup

Only tested on macOS.

1. Ensure you have docker installed.
2. Clone this repository.   
3. Run `make brew_install_kind_and_fluxcd`.

## Create dev kind cluster, install fluxcd, and bootstrap cluster

1. Run `CLUSTER_NAME=dev make kind_cluster_setup`.
2. Run `CLUSTER_NAME=dev make fluxcd_bootstrap`.