KAPITAN_VERSION := v0.29.5
KAPITAN_IMAGE := deepmind/kapitan:$(KAPITAN_VERSION)
KUBECONFIG := $(HOME)/.kube/k8s-kapitan-fluxcd-example-config

.PHONY: help
default: help
help: ## Show this help
	@echo "k8s-kapitan-fluxcd-example"
	@echo "======================"
	@echo
	@echo "A repo to demonstrate kapitan and fluxcd with multiple clusters"
	@echo
	@fgrep -h " ## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -Ee 's/([a-z.]*):[^#]*##(.*)/\1##\2/' | column -t -s "##"

.PHONY: exec
exec: ## docker run the kapitan image and exec into the container
	docker run -it --rm --entrypoint sh -v $(PWD):/src:delegated $(KAPITAN_IMAGE)

.PHONY: compile_fetch
compile_fetch: ## compiles manifests and fetches dependencies for all targets
	docker run --rm -v $(PWD):/src:delegated $(KAPITAN_IMAGE) compile --fetch --force --verbose

.PHONY: brew_install_kind_and_fluxcd
brew_install_kind_and_fluxcd: ## brew installs kind and fluxcd if not present
	brew list kind || brew install kind
	brew list flux || brew install fluxcd/tap/flux

.PHONY: kind_cluster_setup
kind_cluster_setup: ## creates a kind cluster with the provided CLUSTER_NAME and extra config to support ingress https://kind.sigs.k8s.io/docs/user/ingress/
	@[ "${CLUSTER_NAME}" ] || ( echo ">> CLUSTER_NAME is not set"; exit 1 )
	kind create cluster --name $(CLUSTER_NAME) --kubeconfig $(KUBECONFIG) --config=$(PWD)/scripts/kind-config.yml

.PHONY: flux_create_component
flux_create_component: ## uses flux cli to create flux bootstrap manifests referenced by the flux-system component
	@[ "${FLUX_VERSION}" ] || ( echo ">> FLUX_VERSION is not set"; exit 1 )
	FLUX_VERSION_DASH=$(shell echo "$(FLUX_VERSION)" | sed 's/\./-/g'); \
	mkdir -p "components/flux-system/$${FLUX_VERSION_DASH}"; \
	flux install --version=$(FLUX_VERSION) --dry-run --export > "components/flux-system/$${FLUX_VERSION_DASH}/bootstrap.yml"
