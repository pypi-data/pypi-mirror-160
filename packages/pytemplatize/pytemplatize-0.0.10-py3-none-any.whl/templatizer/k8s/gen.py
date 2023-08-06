"""AUTO-GENERATED FILE: DO NOT EDIT"""
# pylint: skip-file
# flake8: noqa

from typing import Any, Dict, List, Literal, Optional

from . import K8STemplatable


class io__k8s__api__admissionregistration__v1__RuleWithOperations(K8STemplatable):
    """RuleWithOperations is a tuple of Operations and Resources. It is recommended to make sure that all the tuple expansions are valid."""

    props: List[str] = ["apiGroups", "apiVersions", "operations", "resources", "scope"]
    required_props: List[str] = []

    @property
    def apiGroups(self) -> Optional[List[str]]:
        return self._apiGroups

    @property
    def apiVersions(self) -> Optional[List[str]]:
        return self._apiVersions

    @property
    def operations(self) -> Optional[List[str]]:
        return self._operations

    @property
    def resources(self) -> Optional[List[str]]:
        return self._resources

    @property
    def scope(self) -> Optional[str]:
        return self._scope

    def __init__(
        self,
        apiGroups: Optional[List[str]] = None,
        apiVersions: Optional[List[str]] = None,
        operations: Optional[List[str]] = None,
        resources: Optional[List[str]] = None,
        scope: Optional[str] = None,
    ):
        super().__init__()
        if apiGroups is not None:
            self._apiGroups = apiGroups
        if apiVersions is not None:
            self._apiVersions = apiVersions
        if operations is not None:
            self._operations = operations
        if resources is not None:
            self._resources = resources
        if scope is not None:
            self._scope = scope


class io__k8s__api__admissionregistration__v1__ServiceReference(K8STemplatable):
    """ServiceReference holds a reference to Service.legacy.k8s.io"""

    props: List[str] = ["name", "namespace", "path", "port"]
    required_props: List[str] = ["namespace", "name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def port(self) -> Optional[int]:
        return self._port

    def __init__(
        self,
        name: str,
        namespace: str,
        path: Optional[str] = None,
        port: Optional[int] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace
        if path is not None:
            self._path = path
        if port is not None:
            self._port = port


class io__k8s__api__admissionregistration__v1__WebhookClientConfig(K8STemplatable):
    """WebhookClientConfig contains the information to make a TLS connection with the webhook"""

    props: List[str] = ["caBundle", "service", "url"]
    required_props: List[str] = []

    @property
    def caBundle(self) -> Optional[str]:
        return self._caBundle

    @property
    def service(
        self,
    ) -> Optional[io__k8s__api__admissionregistration__v1__ServiceReference]:
        return self._service

    @property
    def url(self) -> Optional[str]:
        return self._url

    def __init__(
        self,
        caBundle: Optional[str] = None,
        service: Optional[
            io__k8s__api__admissionregistration__v1__ServiceReference
        ] = None,
        url: Optional[str] = None,
    ):
        super().__init__()
        if caBundle is not None:
            self._caBundle = caBundle
        if service is not None:
            self._service = service
        if url is not None:
            self._url = url


class io__k8s__api__apiserverinternal__v1alpha1__ServerStorageVersion(K8STemplatable):
    """An API server instance reports the version it can decode and the version it encodes objects to when persisting objects in the backend."""

    props: List[str] = ["apiServerID", "decodableVersions", "encodingVersion"]
    required_props: List[str] = []

    @property
    def apiServerID(self) -> Optional[str]:
        return self._apiServerID

    @property
    def decodableVersions(self) -> Optional[List[str]]:
        return self._decodableVersions

    @property
    def encodingVersion(self) -> Optional[str]:
        return self._encodingVersion

    def __init__(
        self,
        apiServerID: Optional[str] = None,
        decodableVersions: Optional[List[str]] = None,
        encodingVersion: Optional[str] = None,
    ):
        super().__init__()
        if apiServerID is not None:
            self._apiServerID = apiServerID
        if decodableVersions is not None:
            self._decodableVersions = decodableVersions
        if encodingVersion is not None:
            self._encodingVersion = encodingVersion


class io__k8s__api__apiserverinternal__v1alpha1__StorageVersionSpec(K8STemplatable):
    """StorageVersionSpec is an empty spec."""

    props: List[str] = []
    required_props: List[str] = []


class io__k8s__api__apps__v1__RollingUpdateStatefulSetStrategy(K8STemplatable):
    """RollingUpdateStatefulSetStrategy is used to communicate parameter for RollingUpdateStatefulSetStrategyType."""

    props: List[str] = ["partition"]
    required_props: List[str] = []

    @property
    def partition(self) -> Optional[int]:
        return self._partition

    def __init__(self, partition: Optional[int] = None):
        super().__init__()
        if partition is not None:
            self._partition = partition


class io__k8s__api__apps__v1__StatefulSetPersistentVolumeClaimRetentionPolicy(
    K8STemplatable
):
    """StatefulSetPersistentVolumeClaimRetentionPolicy describes the policy used for PVCs created from the StatefulSet VolumeClaimTemplates."""

    props: List[str] = ["whenDeleted", "whenScaled"]
    required_props: List[str] = []

    @property
    def whenDeleted(self) -> Optional[str]:
        return self._whenDeleted

    @property
    def whenScaled(self) -> Optional[str]:
        return self._whenScaled

    def __init__(
        self, whenDeleted: Optional[str] = None, whenScaled: Optional[str] = None
    ):
        super().__init__()
        if whenDeleted is not None:
            self._whenDeleted = whenDeleted
        if whenScaled is not None:
            self._whenScaled = whenScaled


class io__k8s__api__apps__v1__StatefulSetUpdateStrategy(K8STemplatable):
    """StatefulSetUpdateStrategy indicates the strategy that the StatefulSet controller will use to perform updates. It includes any additional parameters necessary to perform the update for the indicated strategy."""

    props: List[str] = ["rollingUpdate", "type"]
    required_props: List[str] = []

    @property
    def rollingUpdate(
        self,
    ) -> Optional[io__k8s__api__apps__v1__RollingUpdateStatefulSetStrategy]:
        return self._rollingUpdate

    @property
    def type(self) -> Optional[Literal["OnDelete", "RollingUpdate"]]:
        return self._type

    def __init__(
        self,
        rollingUpdate: Optional[
            io__k8s__api__apps__v1__RollingUpdateStatefulSetStrategy
        ] = None,
        type: Optional[Literal["OnDelete", "RollingUpdate"]] = None,
    ):
        super().__init__()
        if rollingUpdate is not None:
            self._rollingUpdate = rollingUpdate
        if type is not None:
            self._type = type


class io__k8s__api__authentication__v1__BoundObjectReference(K8STemplatable):
    """BoundObjectReference is a reference to an object that a token is bound to."""

    props: List[str] = ["apiVersion", "kind", "name", "uid"]
    required_props: List[str] = []

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @property
    def kind(self) -> Optional[str]:
        return self._kind

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    def __init__(
        self,
        apiVersion: Optional[str] = None,
        kind: Optional[str] = None,
        name: Optional[str] = None,
        uid: Optional[str] = None,
    ):
        super().__init__()
        if apiVersion is not None:
            self._apiVersion = apiVersion
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if uid is not None:
            self._uid = uid


class io__k8s__api__authentication__v1__TokenRequestSpec(K8STemplatable):
    """TokenRequestSpec contains client provided parameters of a token request."""

    props: List[str] = ["audiences", "boundObjectRef", "expirationSeconds"]
    required_props: List[str] = ["audiences"]

    @property
    def audiences(self) -> List[str]:
        return self._audiences

    @property
    def boundObjectRef(
        self,
    ) -> Optional[io__k8s__api__authentication__v1__BoundObjectReference]:
        return self._boundObjectRef

    @property
    def expirationSeconds(self) -> Optional[int]:
        return self._expirationSeconds

    def __init__(
        self,
        audiences: List[str],
        boundObjectRef: Optional[
            io__k8s__api__authentication__v1__BoundObjectReference
        ] = None,
        expirationSeconds: Optional[int] = None,
    ):
        super().__init__()
        if audiences is not None:
            self._audiences = audiences
        if boundObjectRef is not None:
            self._boundObjectRef = boundObjectRef
        if expirationSeconds is not None:
            self._expirationSeconds = expirationSeconds


class io__k8s__api__authentication__v1__TokenReviewSpec(K8STemplatable):
    """TokenReviewSpec is a description of the token authentication request."""

    props: List[str] = ["audiences", "token"]
    required_props: List[str] = []

    @property
    def audiences(self) -> Optional[List[str]]:
        return self._audiences

    @property
    def token(self) -> Optional[str]:
        return self._token

    def __init__(
        self, audiences: Optional[List[str]] = None, token: Optional[str] = None
    ):
        super().__init__()
        if audiences is not None:
            self._audiences = audiences
        if token is not None:
            self._token = token


class io__k8s__api__authentication__v1__UserInfo(K8STemplatable):
    """UserInfo holds the information about the user needed to implement the user.Info interface."""

    props: List[str] = ["extra", "groups", "uid", "username"]
    required_props: List[str] = []

    @property
    def extra(self) -> Optional[Dict[str, List[str]]]:
        return self._extra

    @property
    def groups(self) -> Optional[List[str]]:
        return self._groups

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    @property
    def username(self) -> Optional[str]:
        return self._username

    def __init__(
        self,
        extra: Optional[Dict[str, List[str]]] = None,
        groups: Optional[List[str]] = None,
        uid: Optional[str] = None,
        username: Optional[str] = None,
    ):
        super().__init__()
        if extra is not None:
            self._extra = extra
        if groups is not None:
            self._groups = groups
        if uid is not None:
            self._uid = uid
        if username is not None:
            self._username = username


class io__k8s__api__authorization__v1__NonResourceAttributes(K8STemplatable):
    """NonResourceAttributes includes the authorization attributes available for non-resource requests to the Authorizer interface"""

    props: List[str] = ["path", "verb"]
    required_props: List[str] = []

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def verb(self) -> Optional[str]:
        return self._verb

    def __init__(self, path: Optional[str] = None, verb: Optional[str] = None):
        super().__init__()
        if path is not None:
            self._path = path
        if verb is not None:
            self._verb = verb


class io__k8s__api__authorization__v1__NonResourceRule(K8STemplatable):
    """NonResourceRule holds information that describes a rule for the non-resource"""

    props: List[str] = ["nonResourceURLs", "verbs"]
    required_props: List[str] = ["verbs"]

    @property
    def nonResourceURLs(self) -> Optional[List[str]]:
        return self._nonResourceURLs

    @property
    def verbs(self) -> List[str]:
        return self._verbs

    def __init__(self, verbs: List[str], nonResourceURLs: Optional[List[str]] = None):
        super().__init__()
        if verbs is not None:
            self._verbs = verbs
        if nonResourceURLs is not None:
            self._nonResourceURLs = nonResourceURLs


class io__k8s__api__authorization__v1__ResourceAttributes(K8STemplatable):
    """ResourceAttributes includes the authorization attributes available for resource requests to the Authorizer interface"""

    props: List[str] = [
        "group",
        "name",
        "namespace",
        "resource",
        "subresource",
        "verb",
        "version",
    ]
    required_props: List[str] = []

    @property
    def group(self) -> Optional[str]:
        return self._group

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    @property
    def resource(self) -> Optional[str]:
        return self._resource

    @property
    def subresource(self) -> Optional[str]:
        return self._subresource

    @property
    def verb(self) -> Optional[str]:
        return self._verb

    @property
    def version(self) -> Optional[str]:
        return self._version

    def __init__(
        self,
        group: Optional[str] = None,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        resource: Optional[str] = None,
        subresource: Optional[str] = None,
        verb: Optional[str] = None,
        version: Optional[str] = None,
    ):
        super().__init__()
        if group is not None:
            self._group = group
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace
        if resource is not None:
            self._resource = resource
        if subresource is not None:
            self._subresource = subresource
        if verb is not None:
            self._verb = verb
        if version is not None:
            self._version = version


class io__k8s__api__authorization__v1__ResourceRule(K8STemplatable):
    """ResourceRule is the list of actions the subject is allowed to perform on resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete."""

    props: List[str] = ["apiGroups", "resourceNames", "resources", "verbs"]
    required_props: List[str] = ["verbs"]

    @property
    def apiGroups(self) -> Optional[List[str]]:
        return self._apiGroups

    @property
    def resourceNames(self) -> Optional[List[str]]:
        return self._resourceNames

    @property
    def resources(self) -> Optional[List[str]]:
        return self._resources

    @property
    def verbs(self) -> List[str]:
        return self._verbs

    def __init__(
        self,
        verbs: List[str],
        apiGroups: Optional[List[str]] = None,
        resourceNames: Optional[List[str]] = None,
        resources: Optional[List[str]] = None,
    ):
        super().__init__()
        if verbs is not None:
            self._verbs = verbs
        if apiGroups is not None:
            self._apiGroups = apiGroups
        if resourceNames is not None:
            self._resourceNames = resourceNames
        if resources is not None:
            self._resources = resources


class io__k8s__api__authorization__v1__SelfSubjectAccessReviewSpec(K8STemplatable):
    """SelfSubjectAccessReviewSpec is a description of the access request.  Exactly one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must be set"""

    props: List[str] = ["nonResourceAttributes", "resourceAttributes"]
    required_props: List[str] = []

    @property
    def nonResourceAttributes(
        self,
    ) -> Optional[io__k8s__api__authorization__v1__NonResourceAttributes]:
        return self._nonResourceAttributes

    @property
    def resourceAttributes(
        self,
    ) -> Optional[io__k8s__api__authorization__v1__ResourceAttributes]:
        return self._resourceAttributes

    def __init__(
        self,
        nonResourceAttributes: Optional[
            io__k8s__api__authorization__v1__NonResourceAttributes
        ] = None,
        resourceAttributes: Optional[
            io__k8s__api__authorization__v1__ResourceAttributes
        ] = None,
    ):
        super().__init__()
        if nonResourceAttributes is not None:
            self._nonResourceAttributes = nonResourceAttributes
        if resourceAttributes is not None:
            self._resourceAttributes = resourceAttributes


class io__k8s__api__authorization__v1__SelfSubjectRulesReviewSpec(K8STemplatable):
    """SelfSubjectRulesReviewSpec defines the specification for SelfSubjectRulesReview."""

    props: List[str] = ["namespace"]
    required_props: List[str] = []

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    def __init__(self, namespace: Optional[str] = None):
        super().__init__()
        if namespace is not None:
            self._namespace = namespace


class io__k8s__api__authorization__v1__SubjectAccessReviewSpec(K8STemplatable):
    """SubjectAccessReviewSpec is a description of the access request.  Exactly one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must be set"""

    props: List[str] = [
        "extra",
        "groups",
        "nonResourceAttributes",
        "resourceAttributes",
        "uid",
        "user",
    ]
    required_props: List[str] = []

    @property
    def extra(self) -> Optional[Dict[str, List[str]]]:
        return self._extra

    @property
    def groups(self) -> Optional[List[str]]:
        return self._groups

    @property
    def nonResourceAttributes(
        self,
    ) -> Optional[io__k8s__api__authorization__v1__NonResourceAttributes]:
        return self._nonResourceAttributes

    @property
    def resourceAttributes(
        self,
    ) -> Optional[io__k8s__api__authorization__v1__ResourceAttributes]:
        return self._resourceAttributes

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    @property
    def user(self) -> Optional[str]:
        return self._user

    def __init__(
        self,
        extra: Optional[Dict[str, List[str]]] = None,
        groups: Optional[List[str]] = None,
        nonResourceAttributes: Optional[
            io__k8s__api__authorization__v1__NonResourceAttributes
        ] = None,
        resourceAttributes: Optional[
            io__k8s__api__authorization__v1__ResourceAttributes
        ] = None,
        uid: Optional[str] = None,
        user: Optional[str] = None,
    ):
        super().__init__()
        if extra is not None:
            self._extra = extra
        if groups is not None:
            self._groups = groups
        if nonResourceAttributes is not None:
            self._nonResourceAttributes = nonResourceAttributes
        if resourceAttributes is not None:
            self._resourceAttributes = resourceAttributes
        if uid is not None:
            self._uid = uid
        if user is not None:
            self._user = user


class io__k8s__api__authorization__v1__SubjectAccessReviewStatus(K8STemplatable):
    """SubjectAccessReviewStatus"""

    props: List[str] = ["allowed", "denied", "evaluationError", "reason"]
    required_props: List[str] = ["allowed"]

    @property
    def allowed(self) -> bool:
        return self._allowed

    @property
    def denied(self) -> Optional[bool]:
        return self._denied

    @property
    def evaluationError(self) -> Optional[str]:
        return self._evaluationError

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    def __init__(
        self,
        allowed: bool,
        denied: Optional[bool] = None,
        evaluationError: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if allowed is not None:
            self._allowed = allowed
        if denied is not None:
            self._denied = denied
        if evaluationError is not None:
            self._evaluationError = evaluationError
        if reason is not None:
            self._reason = reason


class io__k8s__api__authorization__v1__SubjectRulesReviewStatus(K8STemplatable):
    """SubjectRulesReviewStatus contains the result of a rules check. This check can be incomplete depending on the set of authorizers the server is configured with and any errors experienced during evaluation. Because authorization rules are additive, if a rule appears in a list it's safe to assume the subject has that permission, even if that list is incomplete."""

    props: List[str] = [
        "evaluationError",
        "incomplete",
        "nonResourceRules",
        "resourceRules",
    ]
    required_props: List[str] = ["resourceRules", "nonResourceRules", "incomplete"]

    @property
    def evaluationError(self) -> Optional[str]:
        return self._evaluationError

    @property
    def incomplete(self) -> bool:
        return self._incomplete

    @property
    def nonResourceRules(
        self,
    ) -> List[io__k8s__api__authorization__v1__NonResourceRule]:
        return self._nonResourceRules

    @property
    def resourceRules(self) -> List[io__k8s__api__authorization__v1__ResourceRule]:
        return self._resourceRules

    def __init__(
        self,
        incomplete: bool,
        nonResourceRules: List[io__k8s__api__authorization__v1__NonResourceRule],
        resourceRules: List[io__k8s__api__authorization__v1__ResourceRule],
        evaluationError: Optional[str] = None,
    ):
        super().__init__()
        if incomplete is not None:
            self._incomplete = incomplete
        if nonResourceRules is not None:
            self._nonResourceRules = nonResourceRules
        if resourceRules is not None:
            self._resourceRules = resourceRules
        if evaluationError is not None:
            self._evaluationError = evaluationError


class io__k8s__api__autoscaling__v1__CrossVersionObjectReference(K8STemplatable):
    """CrossVersionObjectReference contains enough information to let you identify the referred resource."""

    props: List[str] = ["apiVersion", "kind", "name"]
    required_props: List[str] = ["kind", "name"]

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, kind: str, name: str, apiVersion: Optional[str] = None):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if apiVersion is not None:
            self._apiVersion = apiVersion


class io__k8s__api__autoscaling__v1__HorizontalPodAutoscalerSpec(K8STemplatable):
    """specification of a horizontal pod autoscaler."""

    props: List[str] = [
        "maxReplicas",
        "minReplicas",
        "scaleTargetRef",
        "targetCPUUtilizationPercentage",
    ]
    required_props: List[str] = ["scaleTargetRef", "maxReplicas"]

    @property
    def maxReplicas(self) -> int:
        return self._maxReplicas

    @property
    def minReplicas(self) -> Optional[int]:
        return self._minReplicas

    @property
    def scaleTargetRef(
        self,
    ) -> io__k8s__api__autoscaling__v1__CrossVersionObjectReference:
        return self._scaleTargetRef

    @property
    def targetCPUUtilizationPercentage(self) -> Optional[int]:
        return self._targetCPUUtilizationPercentage

    def __init__(
        self,
        maxReplicas: int,
        scaleTargetRef: io__k8s__api__autoscaling__v1__CrossVersionObjectReference,
        minReplicas: Optional[int] = None,
        targetCPUUtilizationPercentage: Optional[int] = None,
    ):
        super().__init__()
        if maxReplicas is not None:
            self._maxReplicas = maxReplicas
        if scaleTargetRef is not None:
            self._scaleTargetRef = scaleTargetRef
        if minReplicas is not None:
            self._minReplicas = minReplicas
        if targetCPUUtilizationPercentage is not None:
            self._targetCPUUtilizationPercentage = targetCPUUtilizationPercentage


class io__k8s__api__autoscaling__v1__ScaleSpec(K8STemplatable):
    """ScaleSpec describes the attributes of a scale subresource."""

    props: List[str] = ["replicas"]
    required_props: List[str] = []

    @property
    def replicas(self) -> Optional[int]:
        return self._replicas

    def __init__(self, replicas: Optional[int] = None):
        super().__init__()
        if replicas is not None:
            self._replicas = replicas


class io__k8s__api__autoscaling__v1__ScaleStatus(K8STemplatable):
    """ScaleStatus represents the current status of a scale subresource."""

    props: List[str] = ["replicas", "selector"]
    required_props: List[str] = ["replicas"]

    @property
    def replicas(self) -> int:
        return self._replicas

    @property
    def selector(self) -> Optional[str]:
        return self._selector

    def __init__(self, replicas: int, selector: Optional[str] = None):
        super().__init__()
        if replicas is not None:
            self._replicas = replicas
        if selector is not None:
            self._selector = selector


class io__k8s__api__autoscaling__v2__CrossVersionObjectReference(K8STemplatable):
    """CrossVersionObjectReference contains enough information to let you identify the referred resource."""

    props: List[str] = ["apiVersion", "kind", "name"]
    required_props: List[str] = ["kind", "name"]

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, kind: str, name: str, apiVersion: Optional[str] = None):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if apiVersion is not None:
            self._apiVersion = apiVersion


class io__k8s__api__autoscaling__v2__HPAScalingPolicy(K8STemplatable):
    """HPAScalingPolicy is a single policy which must hold true for a specified past interval."""

    props: List[str] = ["periodSeconds", "type", "value"]
    required_props: List[str] = ["type", "value", "periodSeconds"]

    @property
    def periodSeconds(self) -> int:
        return self._periodSeconds

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> int:
        return self._value

    def __init__(self, periodSeconds: int, type: str, value: int):
        super().__init__()
        if periodSeconds is not None:
            self._periodSeconds = periodSeconds
        if type is not None:
            self._type = type
        if value is not None:
            self._value = value


class io__k8s__api__autoscaling__v2__HPAScalingRules(K8STemplatable):
    """HPAScalingRules configures the scaling behavior for one direction. These Rules are applied after calculating DesiredReplicas from metrics for the HPA. They can limit the scaling velocity by specifying scaling policies. They can prevent flapping by specifying the stabilization window, so that the number of replicas is not set instantly, instead, the safest value from the stabilization window is chosen."""

    props: List[str] = ["policies", "selectPolicy", "stabilizationWindowSeconds"]
    required_props: List[str] = []

    @property
    def policies(
        self,
    ) -> Optional[List[io__k8s__api__autoscaling__v2__HPAScalingPolicy]]:
        return self._policies

    @property
    def selectPolicy(self) -> Optional[str]:
        return self._selectPolicy

    @property
    def stabilizationWindowSeconds(self) -> Optional[int]:
        return self._stabilizationWindowSeconds

    def __init__(
        self,
        policies: Optional[
            List[io__k8s__api__autoscaling__v2__HPAScalingPolicy]
        ] = None,
        selectPolicy: Optional[str] = None,
        stabilizationWindowSeconds: Optional[int] = None,
    ):
        super().__init__()
        if policies is not None:
            self._policies = policies
        if selectPolicy is not None:
            self._selectPolicy = selectPolicy
        if stabilizationWindowSeconds is not None:
            self._stabilizationWindowSeconds = stabilizationWindowSeconds


class io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerBehavior(K8STemplatable):
    """HorizontalPodAutoscalerBehavior configures the scaling behavior of the target in both Up and Down directions (scaleUp and scaleDown fields respectively)."""

    props: List[str] = ["scaleDown", "scaleUp"]
    required_props: List[str] = []

    @property
    def scaleDown(self) -> Optional[io__k8s__api__autoscaling__v2__HPAScalingRules]:
        return self._scaleDown

    @property
    def scaleUp(self) -> Optional[io__k8s__api__autoscaling__v2__HPAScalingRules]:
        return self._scaleUp

    def __init__(
        self,
        scaleDown: Optional[io__k8s__api__autoscaling__v2__HPAScalingRules] = None,
        scaleUp: Optional[io__k8s__api__autoscaling__v2__HPAScalingRules] = None,
    ):
        super().__init__()
        if scaleDown is not None:
            self._scaleDown = scaleDown
        if scaleUp is not None:
            self._scaleUp = scaleUp


class io__k8s__api__autoscaling__v2beta1__CrossVersionObjectReference(K8STemplatable):
    """CrossVersionObjectReference contains enough information to let you identify the referred resource."""

    props: List[str] = ["apiVersion", "kind", "name"]
    required_props: List[str] = ["kind", "name"]

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, kind: str, name: str, apiVersion: Optional[str] = None):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if apiVersion is not None:
            self._apiVersion = apiVersion


class io__k8s__api__autoscaling__v2beta2__CrossVersionObjectReference(K8STemplatable):
    """CrossVersionObjectReference contains enough information to let you identify the referred resource."""

    props: List[str] = ["apiVersion", "kind", "name"]
    required_props: List[str] = ["kind", "name"]

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, kind: str, name: str, apiVersion: Optional[str] = None):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if apiVersion is not None:
            self._apiVersion = apiVersion


class io__k8s__api__autoscaling__v2beta2__HPAScalingPolicy(K8STemplatable):
    """HPAScalingPolicy is a single policy which must hold true for a specified past interval."""

    props: List[str] = ["periodSeconds", "type", "value"]
    required_props: List[str] = ["type", "value", "periodSeconds"]

    @property
    def periodSeconds(self) -> int:
        return self._periodSeconds

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> int:
        return self._value

    def __init__(self, periodSeconds: int, type: str, value: int):
        super().__init__()
        if periodSeconds is not None:
            self._periodSeconds = periodSeconds
        if type is not None:
            self._type = type
        if value is not None:
            self._value = value


class io__k8s__api__autoscaling__v2beta2__HPAScalingRules(K8STemplatable):
    """HPAScalingRules configures the scaling behavior for one direction. These Rules are applied after calculating DesiredReplicas from metrics for the HPA. They can limit the scaling velocity by specifying scaling policies. They can prevent flapping by specifying the stabilization window, so that the number of replicas is not set instantly, instead, the safest value from the stabilization window is chosen."""

    props: List[str] = ["policies", "selectPolicy", "stabilizationWindowSeconds"]
    required_props: List[str] = []

    @property
    def policies(
        self,
    ) -> Optional[List[io__k8s__api__autoscaling__v2beta2__HPAScalingPolicy]]:
        return self._policies

    @property
    def selectPolicy(self) -> Optional[str]:
        return self._selectPolicy

    @property
    def stabilizationWindowSeconds(self) -> Optional[int]:
        return self._stabilizationWindowSeconds

    def __init__(
        self,
        policies: Optional[
            List[io__k8s__api__autoscaling__v2beta2__HPAScalingPolicy]
        ] = None,
        selectPolicy: Optional[str] = None,
        stabilizationWindowSeconds: Optional[int] = None,
    ):
        super().__init__()
        if policies is not None:
            self._policies = policies
        if selectPolicy is not None:
            self._selectPolicy = selectPolicy
        if stabilizationWindowSeconds is not None:
            self._stabilizationWindowSeconds = stabilizationWindowSeconds


class io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerBehavior(
    K8STemplatable
):
    """HorizontalPodAutoscalerBehavior configures the scaling behavior of the target in both Up and Down directions (scaleUp and scaleDown fields respectively)."""

    props: List[str] = ["scaleDown", "scaleUp"]
    required_props: List[str] = []

    @property
    def scaleDown(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__HPAScalingRules]:
        return self._scaleDown

    @property
    def scaleUp(self) -> Optional[io__k8s__api__autoscaling__v2beta2__HPAScalingRules]:
        return self._scaleUp

    def __init__(
        self,
        scaleDown: Optional[io__k8s__api__autoscaling__v2beta2__HPAScalingRules] = None,
        scaleUp: Optional[io__k8s__api__autoscaling__v2beta2__HPAScalingRules] = None,
    ):
        super().__init__()
        if scaleDown is not None:
            self._scaleDown = scaleDown
        if scaleUp is not None:
            self._scaleUp = scaleUp


class io__k8s__api__batch__v1__UncountedTerminatedPods(K8STemplatable):
    """UncountedTerminatedPods holds UIDs of Pods that have terminated but haven't been accounted in Job status counters."""

    props: List[str] = ["failed", "succeeded"]
    required_props: List[str] = []

    @property
    def failed(self) -> Optional[List[str]]:
        return self._failed

    @property
    def succeeded(self) -> Optional[List[str]]:
        return self._succeeded

    def __init__(
        self, failed: Optional[List[str]] = None, succeeded: Optional[List[str]] = None
    ):
        super().__init__()
        if failed is not None:
            self._failed = failed
        if succeeded is not None:
            self._succeeded = succeeded


class io__k8s__api__certificates__v1__CertificateSigningRequestSpec(K8STemplatable):
    """CertificateSigningRequestSpec contains the certificate request."""

    props: List[str] = [
        "expirationSeconds",
        "extra",
        "groups",
        "request",
        "signerName",
        "uid",
        "usages",
        "username",
    ]
    required_props: List[str] = ["request", "signerName"]

    @property
    def expirationSeconds(self) -> Optional[int]:
        return self._expirationSeconds

    @property
    def extra(self) -> Optional[Dict[str, List[str]]]:
        return self._extra

    @property
    def groups(self) -> Optional[List[str]]:
        return self._groups

    @property
    def request(self) -> str:
        return self._request

    @property
    def signerName(self) -> str:
        return self._signerName

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    @property
    def usages(self) -> Optional[List[str]]:
        return self._usages

    @property
    def username(self) -> Optional[str]:
        return self._username

    def __init__(
        self,
        request: str,
        signerName: str,
        expirationSeconds: Optional[int] = None,
        extra: Optional[Dict[str, List[str]]] = None,
        groups: Optional[List[str]] = None,
        uid: Optional[str] = None,
        usages: Optional[List[str]] = None,
        username: Optional[str] = None,
    ):
        super().__init__()
        if request is not None:
            self._request = request
        if signerName is not None:
            self._signerName = signerName
        if expirationSeconds is not None:
            self._expirationSeconds = expirationSeconds
        if extra is not None:
            self._extra = extra
        if groups is not None:
            self._groups = groups
        if uid is not None:
            self._uid = uid
        if usages is not None:
            self._usages = usages
        if username is not None:
            self._username = username


class io__k8s__api__core__v1__AWSElasticBlockStoreVolumeSource(K8STemplatable):
    """Represents a Persistent Disk resource in AWS.

    An AWS EBS disk must exist before mounting to a container. The disk must also be in the same AWS zone as the kubelet. An AWS EBS disk can only be mounted as read/write once. AWS EBS volumes support ownership management and SELinux relabeling."""

    props: List[str] = ["fsType", "partition", "readOnly", "volumeID"]
    required_props: List[str] = ["volumeID"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def partition(self) -> Optional[int]:
        return self._partition

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def volumeID(self) -> str:
        return self._volumeID

    def __init__(
        self,
        volumeID: str,
        fsType: Optional[str] = None,
        partition: Optional[int] = None,
        readOnly: Optional[bool] = None,
    ):
        super().__init__()
        if volumeID is not None:
            self._volumeID = volumeID
        if fsType is not None:
            self._fsType = fsType
        if partition is not None:
            self._partition = partition
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__AttachedVolume(K8STemplatable):
    """AttachedVolume describes a volume attached to a node"""

    props: List[str] = ["devicePath", "name"]
    required_props: List[str] = ["name", "devicePath"]

    @property
    def devicePath(self) -> str:
        return self._devicePath

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, devicePath: str, name: str):
        super().__init__()
        if devicePath is not None:
            self._devicePath = devicePath
        if name is not None:
            self._name = name


class io__k8s__api__core__v1__AzureDiskVolumeSource(K8STemplatable):
    """AzureDisk represents an Azure Data Disk mount on the host and bind mount to the pod."""

    props: List[str] = [
        "cachingMode",
        "diskName",
        "diskURI",
        "fsType",
        "kind",
        "readOnly",
    ]
    required_props: List[str] = ["diskName", "diskURI"]

    @property
    def cachingMode(self) -> Optional[str]:
        return self._cachingMode

    @property
    def diskName(self) -> str:
        return self._diskName

    @property
    def diskURI(self) -> str:
        return self._diskURI

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def kind(self) -> Optional[str]:
        return self._kind

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    def __init__(
        self,
        diskName: str,
        diskURI: str,
        cachingMode: Optional[str] = None,
        fsType: Optional[str] = None,
        kind: Optional[str] = None,
        readOnly: Optional[bool] = None,
    ):
        super().__init__()
        if diskName is not None:
            self._diskName = diskName
        if diskURI is not None:
            self._diskURI = diskURI
        if cachingMode is not None:
            self._cachingMode = cachingMode
        if fsType is not None:
            self._fsType = fsType
        if kind is not None:
            self._kind = kind
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__AzureFilePersistentVolumeSource(K8STemplatable):
    """AzureFile represents an Azure File Service mount on the host and bind mount to the pod."""

    props: List[str] = ["readOnly", "secretName", "secretNamespace", "shareName"]
    required_props: List[str] = ["secretName", "shareName"]

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretName(self) -> str:
        return self._secretName

    @property
    def secretNamespace(self) -> Optional[str]:
        return self._secretNamespace

    @property
    def shareName(self) -> str:
        return self._shareName

    def __init__(
        self,
        secretName: str,
        shareName: str,
        readOnly: Optional[bool] = None,
        secretNamespace: Optional[str] = None,
    ):
        super().__init__()
        if secretName is not None:
            self._secretName = secretName
        if shareName is not None:
            self._shareName = shareName
        if readOnly is not None:
            self._readOnly = readOnly
        if secretNamespace is not None:
            self._secretNamespace = secretNamespace


class io__k8s__api__core__v1__AzureFileVolumeSource(K8STemplatable):
    """AzureFile represents an Azure File Service mount on the host and bind mount to the pod."""

    props: List[str] = ["readOnly", "secretName", "shareName"]
    required_props: List[str] = ["secretName", "shareName"]

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretName(self) -> str:
        return self._secretName

    @property
    def shareName(self) -> str:
        return self._shareName

    def __init__(
        self, secretName: str, shareName: str, readOnly: Optional[bool] = None
    ):
        super().__init__()
        if secretName is not None:
            self._secretName = secretName
        if shareName is not None:
            self._shareName = shareName
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__Capabilities(K8STemplatable):
    """Adds and removes POSIX capabilities from running containers."""

    props: List[str] = ["add", "drop"]
    required_props: List[str] = []

    @property
    def add(self) -> Optional[List[str]]:
        return self._add

    @property
    def drop(self) -> Optional[List[str]]:
        return self._drop

    def __init__(
        self, add: Optional[List[str]] = None, drop: Optional[List[str]] = None
    ):
        super().__init__()
        if add is not None:
            self._add = add
        if drop is not None:
            self._drop = drop


class io__k8s__api__core__v1__ClientIPConfig(K8STemplatable):
    """ClientIPConfig represents the configurations of Client IP based session affinity."""

    props: List[str] = ["timeoutSeconds"]
    required_props: List[str] = []

    @property
    def timeoutSeconds(self) -> Optional[int]:
        return self._timeoutSeconds

    def __init__(self, timeoutSeconds: Optional[int] = None):
        super().__init__()
        if timeoutSeconds is not None:
            self._timeoutSeconds = timeoutSeconds


class io__k8s__api__core__v1__ComponentCondition(K8STemplatable):
    """Information about the condition of a component."""

    props: List[str] = ["error", "message", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def error(self) -> Optional[str]:
        return self._error

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        error: Optional[str] = None,
        message: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if error is not None:
            self._error = error
        if message is not None:
            self._message = message


class io__k8s__api__core__v1__ConfigMapEnvSource(K8STemplatable):
    """ConfigMapEnvSource selects a ConfigMap to populate the environment variables with.

    The contents of the target ConfigMap's Data field will represent the key-value pairs as environment variables."""

    props: List[str] = ["name", "optional"]
    required_props: List[str] = []

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def optional(self) -> Optional[bool]:
        return self._optional

    def __init__(self, name: Optional[str] = None, optional: Optional[bool] = None):
        super().__init__()
        if name is not None:
            self._name = name
        if optional is not None:
            self._optional = optional


class io__k8s__api__core__v1__ConfigMapKeySelector(K8STemplatable):
    """Selects a key from a ConfigMap."""

    props: List[str] = ["key", "name", "optional"]
    required_props: List[str] = ["key"]

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def optional(self) -> Optional[bool]:
        return self._optional

    def __init__(
        self, key: str, name: Optional[str] = None, optional: Optional[bool] = None
    ):
        super().__init__()
        if key is not None:
            self._key = key
        if name is not None:
            self._name = name
        if optional is not None:
            self._optional = optional


class io__k8s__api__core__v1__ConfigMapNodeConfigSource(K8STemplatable):
    """ConfigMapNodeConfigSource contains the information to reference a ConfigMap as a config source for the Node. This API is deprecated since 1.22: https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration"""

    props: List[str] = [
        "kubeletConfigKey",
        "name",
        "namespace",
        "resourceVersion",
        "uid",
    ]
    required_props: List[str] = ["namespace", "name", "kubeletConfigKey"]

    @property
    def kubeletConfigKey(self) -> str:
        return self._kubeletConfigKey

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def resourceVersion(self) -> Optional[str]:
        return self._resourceVersion

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    def __init__(
        self,
        kubeletConfigKey: str,
        name: str,
        namespace: str,
        resourceVersion: Optional[str] = None,
        uid: Optional[str] = None,
    ):
        super().__init__()
        if kubeletConfigKey is not None:
            self._kubeletConfigKey = kubeletConfigKey
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace
        if resourceVersion is not None:
            self._resourceVersion = resourceVersion
        if uid is not None:
            self._uid = uid


class io__k8s__api__core__v1__ContainerImage(K8STemplatable):
    """Describe a container image"""

    props: List[str] = ["names", "sizeBytes"]
    required_props: List[str] = []

    @property
    def names(self) -> Optional[List[str]]:
        return self._names

    @property
    def sizeBytes(self) -> Optional[int]:
        return self._sizeBytes

    def __init__(
        self, names: Optional[List[str]] = None, sizeBytes: Optional[int] = None
    ):
        super().__init__()
        if names is not None:
            self._names = names
        if sizeBytes is not None:
            self._sizeBytes = sizeBytes


class io__k8s__api__core__v1__ContainerPort(K8STemplatable):
    """ContainerPort represents a network port in a single container."""

    props: List[str] = ["containerPort", "hostIP", "hostPort", "name", "protocol"]
    required_props: List[str] = ["containerPort"]

    @property
    def containerPort(self) -> int:
        return self._containerPort

    @property
    def hostIP(self) -> Optional[str]:
        return self._hostIP

    @property
    def hostPort(self) -> Optional[int]:
        return self._hostPort

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def protocol(self) -> Optional[Literal["SCTP", "TCP", "UDP"]]:
        return self._protocol

    def __init__(
        self,
        containerPort: int,
        hostIP: Optional[str] = None,
        hostPort: Optional[int] = None,
        name: Optional[str] = None,
        protocol: Optional[Literal["SCTP", "TCP", "UDP"]] = None,
    ):
        super().__init__()
        if containerPort is not None:
            self._containerPort = containerPort
        if hostIP is not None:
            self._hostIP = hostIP
        if hostPort is not None:
            self._hostPort = hostPort
        if name is not None:
            self._name = name
        if protocol is not None:
            self._protocol = protocol


class io__k8s__api__core__v1__ContainerStateWaiting(K8STemplatable):
    """ContainerStateWaiting is a waiting state of a container."""

    props: List[str] = ["message", "reason"]
    required_props: List[str] = []

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    def __init__(self, message: Optional[str] = None, reason: Optional[str] = None):
        super().__init__()
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__core__v1__DaemonEndpoint(K8STemplatable):
    """DaemonEndpoint contains information about a single Daemon endpoint."""

    props: List[str] = ["Port"]
    required_props: List[str] = ["Port"]

    @property
    def Port(self) -> int:
        return self._Port

    def __init__(self, Port: int):
        super().__init__()
        if Port is not None:
            self._Port = Port


class io__k8s__api__core__v1__EndpointPort(K8STemplatable):
    """EndpointPort is a tuple that describes a single port."""

    props: List[str] = ["appProtocol", "name", "port", "protocol"]
    required_props: List[str] = ["port"]

    @property
    def appProtocol(self) -> Optional[str]:
        return self._appProtocol

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def port(self) -> int:
        return self._port

    @property
    def protocol(self) -> Optional[Literal["SCTP", "TCP", "UDP"]]:
        return self._protocol

    def __init__(
        self,
        port: int,
        appProtocol: Optional[str] = None,
        name: Optional[str] = None,
        protocol: Optional[Literal["SCTP", "TCP", "UDP"]] = None,
    ):
        super().__init__()
        if port is not None:
            self._port = port
        if appProtocol is not None:
            self._appProtocol = appProtocol
        if name is not None:
            self._name = name
        if protocol is not None:
            self._protocol = protocol


class io__k8s__api__core__v1__EventSource(K8STemplatable):
    """EventSource contains information for an event."""

    props: List[str] = ["component", "host"]
    required_props: List[str] = []

    @property
    def component(self) -> Optional[str]:
        return self._component

    @property
    def host(self) -> Optional[str]:
        return self._host

    def __init__(self, component: Optional[str] = None, host: Optional[str] = None):
        super().__init__()
        if component is not None:
            self._component = component
        if host is not None:
            self._host = host


class io__k8s__api__core__v1__ExecAction(K8STemplatable):
    """ExecAction describes a "run in container" action."""

    props: List[str] = ["command"]
    required_props: List[str] = []

    @property
    def command(self) -> Optional[List[str]]:
        return self._command

    def __init__(self, command: Optional[List[str]] = None):
        super().__init__()
        if command is not None:
            self._command = command


class io__k8s__api__core__v1__FCVolumeSource(K8STemplatable):
    """Represents a Fibre Channel volume. Fibre Channel volumes can only be mounted as read/write once. Fibre Channel volumes support ownership management and SELinux relabeling."""

    props: List[str] = ["fsType", "lun", "readOnly", "targetWWNs", "wwids"]
    required_props: List[str] = []

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def lun(self) -> Optional[int]:
        return self._lun

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def targetWWNs(self) -> Optional[List[str]]:
        return self._targetWWNs

    @property
    def wwids(self) -> Optional[List[str]]:
        return self._wwids

    def __init__(
        self,
        fsType: Optional[str] = None,
        lun: Optional[int] = None,
        readOnly: Optional[bool] = None,
        targetWWNs: Optional[List[str]] = None,
        wwids: Optional[List[str]] = None,
    ):
        super().__init__()
        if fsType is not None:
            self._fsType = fsType
        if lun is not None:
            self._lun = lun
        if readOnly is not None:
            self._readOnly = readOnly
        if targetWWNs is not None:
            self._targetWWNs = targetWWNs
        if wwids is not None:
            self._wwids = wwids


class io__k8s__api__core__v1__FlockerVolumeSource(K8STemplatable):
    """Represents a Flocker volume mounted by the Flocker agent. One and only one of datasetName and datasetUUID should be set. Flocker volumes do not support ownership management or SELinux relabeling."""

    props: List[str] = ["datasetName", "datasetUUID"]
    required_props: List[str] = []

    @property
    def datasetName(self) -> Optional[str]:
        return self._datasetName

    @property
    def datasetUUID(self) -> Optional[str]:
        return self._datasetUUID

    def __init__(
        self, datasetName: Optional[str] = None, datasetUUID: Optional[str] = None
    ):
        super().__init__()
        if datasetName is not None:
            self._datasetName = datasetName
        if datasetUUID is not None:
            self._datasetUUID = datasetUUID


class io__k8s__api__core__v1__GCEPersistentDiskVolumeSource(K8STemplatable):
    """Represents a Persistent Disk resource in Google Compute Engine.

    A GCE PD must exist before mounting to a container. The disk must also be in the same GCE project and zone as the kubelet. A GCE PD can only be mounted as read/write once or read-only many times. GCE PDs support ownership management and SELinux relabeling."""

    props: List[str] = ["fsType", "partition", "pdName", "readOnly"]
    required_props: List[str] = ["pdName"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def partition(self) -> Optional[int]:
        return self._partition

    @property
    def pdName(self) -> str:
        return self._pdName

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    def __init__(
        self,
        pdName: str,
        fsType: Optional[str] = None,
        partition: Optional[int] = None,
        readOnly: Optional[bool] = None,
    ):
        super().__init__()
        if pdName is not None:
            self._pdName = pdName
        if fsType is not None:
            self._fsType = fsType
        if partition is not None:
            self._partition = partition
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__GRPCAction(K8STemplatable):
    """None"""

    props: List[str] = ["port", "service"]
    required_props: List[str] = ["port"]

    @property
    def port(self) -> int:
        return self._port

    @property
    def service(self) -> Optional[str]:
        return self._service

    def __init__(self, port: int, service: Optional[str] = None):
        super().__init__()
        if port is not None:
            self._port = port
        if service is not None:
            self._service = service


class io__k8s__api__core__v1__GitRepoVolumeSource(K8STemplatable):
    """Represents a volume that is populated with the contents of a git repository. Git repo volumes do not support ownership management. Git repo volumes support SELinux relabeling.

    DEPRECATED: GitRepo is deprecated. To provision a container with a git repo, mount an EmptyDir into an InitContainer that clones the repo using git, then mount the EmptyDir into the Pod's container."""

    props: List[str] = ["directory", "repository", "revision"]
    required_props: List[str] = ["repository"]

    @property
    def directory(self) -> Optional[str]:
        return self._directory

    @property
    def repository(self) -> str:
        return self._repository

    @property
    def revision(self) -> Optional[str]:
        return self._revision

    def __init__(
        self,
        repository: str,
        directory: Optional[str] = None,
        revision: Optional[str] = None,
    ):
        super().__init__()
        if repository is not None:
            self._repository = repository
        if directory is not None:
            self._directory = directory
        if revision is not None:
            self._revision = revision


class io__k8s__api__core__v1__GlusterfsPersistentVolumeSource(K8STemplatable):
    """Represents a Glusterfs mount that lasts the lifetime of a pod. Glusterfs volumes do not support ownership management or SELinux relabeling."""

    props: List[str] = ["endpoints", "endpointsNamespace", "path", "readOnly"]
    required_props: List[str] = ["endpoints", "path"]

    @property
    def endpoints(self) -> str:
        return self._endpoints

    @property
    def endpointsNamespace(self) -> Optional[str]:
        return self._endpointsNamespace

    @property
    def path(self) -> str:
        return self._path

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    def __init__(
        self,
        endpoints: str,
        path: str,
        endpointsNamespace: Optional[str] = None,
        readOnly: Optional[bool] = None,
    ):
        super().__init__()
        if endpoints is not None:
            self._endpoints = endpoints
        if path is not None:
            self._path = path
        if endpointsNamespace is not None:
            self._endpointsNamespace = endpointsNamespace
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__GlusterfsVolumeSource(K8STemplatable):
    """Represents a Glusterfs mount that lasts the lifetime of a pod. Glusterfs volumes do not support ownership management or SELinux relabeling."""

    props: List[str] = ["endpoints", "path", "readOnly"]
    required_props: List[str] = ["endpoints", "path"]

    @property
    def endpoints(self) -> str:
        return self._endpoints

    @property
    def path(self) -> str:
        return self._path

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    def __init__(self, endpoints: str, path: str, readOnly: Optional[bool] = None):
        super().__init__()
        if endpoints is not None:
            self._endpoints = endpoints
        if path is not None:
            self._path = path
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__HTTPHeader(K8STemplatable):
    """HTTPHeader describes a custom header to be used in HTTP probes"""

    props: List[str] = ["name", "value"]
    required_props: List[str] = ["name", "value"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    def __init__(self, name: str, value: str):
        super().__init__()
        if name is not None:
            self._name = name
        if value is not None:
            self._value = value


class io__k8s__api__core__v1__HostAlias(K8STemplatable):
    """HostAlias holds the mapping between IP and hostnames that will be injected as an entry in the pod's hosts file."""

    props: List[str] = ["hostnames", "ip"]
    required_props: List[str] = []

    @property
    def hostnames(self) -> Optional[List[str]]:
        return self._hostnames

    @property
    def ip(self) -> Optional[str]:
        return self._ip

    def __init__(self, hostnames: Optional[List[str]] = None, ip: Optional[str] = None):
        super().__init__()
        if hostnames is not None:
            self._hostnames = hostnames
        if ip is not None:
            self._ip = ip


class io__k8s__api__core__v1__HostPathVolumeSource(K8STemplatable):
    """Represents a host path mapped into a pod. Host path volumes do not support ownership management or SELinux relabeling."""

    props: List[str] = ["path", "type"]
    required_props: List[str] = ["path"]

    @property
    def path(self) -> str:
        return self._path

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(self, path: str, type: Optional[str] = None):
        super().__init__()
        if path is not None:
            self._path = path
        if type is not None:
            self._type = type


class io__k8s__api__core__v1__KeyToPath(K8STemplatable):
    """Maps a string key to a path within a volume."""

    props: List[str] = ["key", "mode", "path"]
    required_props: List[str] = ["key", "path"]

    @property
    def key(self) -> str:
        return self._key

    @property
    def mode(self) -> Optional[int]:
        return self._mode

    @property
    def path(self) -> str:
        return self._path

    def __init__(self, key: str, path: str, mode: Optional[int] = None):
        super().__init__()
        if key is not None:
            self._key = key
        if path is not None:
            self._path = path
        if mode is not None:
            self._mode = mode


class io__k8s__api__core__v1__LocalObjectReference(K8STemplatable):
    """LocalObjectReference contains enough information to let you locate the referenced object inside the same namespace."""

    props: List[str] = ["name"]
    required_props: List[str] = []

    @property
    def name(self) -> Optional[str]:
        return self._name

    def __init__(self, name: Optional[str] = None):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__core__v1__LocalVolumeSource(K8STemplatable):
    """Local represents directly-attached storage with node affinity (Beta feature)"""

    props: List[str] = ["fsType", "path"]
    required_props: List[str] = ["path"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def path(self) -> str:
        return self._path

    def __init__(self, path: str, fsType: Optional[str] = None):
        super().__init__()
        if path is not None:
            self._path = path
        if fsType is not None:
            self._fsType = fsType


class io__k8s__api__core__v1__NFSVolumeSource(K8STemplatable):
    """Represents an NFS mount that lasts the lifetime of a pod. NFS volumes do not support ownership management or SELinux relabeling."""

    props: List[str] = ["path", "readOnly", "server"]
    required_props: List[str] = ["server", "path"]

    @property
    def path(self) -> str:
        return self._path

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def server(self) -> str:
        return self._server

    def __init__(self, path: str, server: str, readOnly: Optional[bool] = None):
        super().__init__()
        if path is not None:
            self._path = path
        if server is not None:
            self._server = server
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__NamespaceSpec(K8STemplatable):
    """NamespaceSpec describes the attributes on a Namespace."""

    props: List[str] = ["finalizers"]
    required_props: List[str] = []

    @property
    def finalizers(self) -> Optional[List[str]]:
        return self._finalizers

    def __init__(self, finalizers: Optional[List[str]] = None):
        super().__init__()
        if finalizers is not None:
            self._finalizers = finalizers


class io__k8s__api__core__v1__NodeAddress(K8STemplatable):
    """NodeAddress contains information for the node's address."""

    props: List[str] = ["address", "type"]
    required_props: List[str] = ["type", "address"]

    @property
    def address(self) -> str:
        return self._address

    @property
    def type(self) -> str:
        return self._type

    def __init__(self, address: str, type: str):
        super().__init__()
        if address is not None:
            self._address = address
        if type is not None:
            self._type = type


class io__k8s__api__core__v1__NodeConfigSource(K8STemplatable):
    """NodeConfigSource specifies a source of node configuration. Exactly one subfield (excluding metadata) must be non-nil. This API is deprecated since 1.22"""

    props: List[str] = ["configMap"]
    required_props: List[str] = []

    @property
    def configMap(self) -> Optional[io__k8s__api__core__v1__ConfigMapNodeConfigSource]:
        return self._configMap

    def __init__(
        self,
        configMap: Optional[io__k8s__api__core__v1__ConfigMapNodeConfigSource] = None,
    ):
        super().__init__()
        if configMap is not None:
            self._configMap = configMap


class io__k8s__api__core__v1__NodeConfigStatus(K8STemplatable):
    """NodeConfigStatus describes the status of the config assigned by Node.Spec.ConfigSource."""

    props: List[str] = ["active", "assigned", "error", "lastKnownGood"]
    required_props: List[str] = []

    @property
    def active(self) -> Optional[io__k8s__api__core__v1__NodeConfigSource]:
        return self._active

    @property
    def assigned(self) -> Optional[io__k8s__api__core__v1__NodeConfigSource]:
        return self._assigned

    @property
    def error(self) -> Optional[str]:
        return self._error

    @property
    def lastKnownGood(self) -> Optional[io__k8s__api__core__v1__NodeConfigSource]:
        return self._lastKnownGood

    def __init__(
        self,
        active: Optional[io__k8s__api__core__v1__NodeConfigSource] = None,
        assigned: Optional[io__k8s__api__core__v1__NodeConfigSource] = None,
        error: Optional[str] = None,
        lastKnownGood: Optional[io__k8s__api__core__v1__NodeConfigSource] = None,
    ):
        super().__init__()
        if active is not None:
            self._active = active
        if assigned is not None:
            self._assigned = assigned
        if error is not None:
            self._error = error
        if lastKnownGood is not None:
            self._lastKnownGood = lastKnownGood


class io__k8s__api__core__v1__NodeDaemonEndpoints(K8STemplatable):
    """NodeDaemonEndpoints lists ports opened by daemons running on the Node."""

    props: List[str] = ["kubeletEndpoint"]
    required_props: List[str] = []

    @property
    def kubeletEndpoint(self) -> Optional[io__k8s__api__core__v1__DaemonEndpoint]:
        return self._kubeletEndpoint

    def __init__(
        self, kubeletEndpoint: Optional[io__k8s__api__core__v1__DaemonEndpoint] = None
    ):
        super().__init__()
        if kubeletEndpoint is not None:
            self._kubeletEndpoint = kubeletEndpoint


class io__k8s__api__core__v1__NodeSelectorRequirement(K8STemplatable):
    """A node selector requirement is a selector that contains values, a key, and an operator that relates the key and values."""

    props: List[str] = ["key", "operator", "values"]
    required_props: List[str] = ["key", "operator"]

    @property
    def key(self) -> str:
        return self._key

    @property
    def operator(self) -> Literal["DoesNotExist", "Exists", "Gt", "In", "Lt", "NotIn"]:
        return self._operator

    @property
    def values(self) -> Optional[List[str]]:
        return self._values

    def __init__(
        self,
        key: str,
        operator: Literal["DoesNotExist", "Exists", "Gt", "In", "Lt", "NotIn"],
        values: Optional[List[str]] = None,
    ):
        super().__init__()
        if key is not None:
            self._key = key
        if operator is not None:
            self._operator = operator
        if values is not None:
            self._values = values


class io__k8s__api__core__v1__NodeSelectorTerm(K8STemplatable):
    """A null or empty node selector term matches no objects. The requirements of them are ANDed. The TopologySelectorTerm type implements a subset of the NodeSelectorTerm."""

    props: List[str] = ["matchExpressions", "matchFields"]
    required_props: List[str] = []

    @property
    def matchExpressions(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__NodeSelectorRequirement]]:
        return self._matchExpressions

    @property
    def matchFields(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__NodeSelectorRequirement]]:
        return self._matchFields

    def __init__(
        self,
        matchExpressions: Optional[
            List[io__k8s__api__core__v1__NodeSelectorRequirement]
        ] = None,
        matchFields: Optional[
            List[io__k8s__api__core__v1__NodeSelectorRequirement]
        ] = None,
    ):
        super().__init__()
        if matchExpressions is not None:
            self._matchExpressions = matchExpressions
        if matchFields is not None:
            self._matchFields = matchFields


class io__k8s__api__core__v1__NodeSystemInfo(K8STemplatable):
    """NodeSystemInfo is a set of ids/uuids to uniquely identify the node."""

    props: List[str] = [
        "architecture",
        "bootID",
        "containerRuntimeVersion",
        "kernelVersion",
        "kubeProxyVersion",
        "kubeletVersion",
        "machineID",
        "operatingSystem",
        "osImage",
        "systemUUID",
    ]
    required_props: List[str] = [
        "machineID",
        "systemUUID",
        "bootID",
        "kernelVersion",
        "osImage",
        "containerRuntimeVersion",
        "kubeletVersion",
        "kubeProxyVersion",
        "operatingSystem",
        "architecture",
    ]

    @property
    def architecture(self) -> str:
        return self._architecture

    @property
    def bootID(self) -> str:
        return self._bootID

    @property
    def containerRuntimeVersion(self) -> str:
        return self._containerRuntimeVersion

    @property
    def kernelVersion(self) -> str:
        return self._kernelVersion

    @property
    def kubeProxyVersion(self) -> str:
        return self._kubeProxyVersion

    @property
    def kubeletVersion(self) -> str:
        return self._kubeletVersion

    @property
    def machineID(self) -> str:
        return self._machineID

    @property
    def operatingSystem(self) -> str:
        return self._operatingSystem

    @property
    def osImage(self) -> str:
        return self._osImage

    @property
    def systemUUID(self) -> str:
        return self._systemUUID

    def __init__(
        self,
        architecture: str,
        bootID: str,
        containerRuntimeVersion: str,
        kernelVersion: str,
        kubeProxyVersion: str,
        kubeletVersion: str,
        machineID: str,
        operatingSystem: str,
        osImage: str,
        systemUUID: str,
    ):
        super().__init__()
        if architecture is not None:
            self._architecture = architecture
        if bootID is not None:
            self._bootID = bootID
        if containerRuntimeVersion is not None:
            self._containerRuntimeVersion = containerRuntimeVersion
        if kernelVersion is not None:
            self._kernelVersion = kernelVersion
        if kubeProxyVersion is not None:
            self._kubeProxyVersion = kubeProxyVersion
        if kubeletVersion is not None:
            self._kubeletVersion = kubeletVersion
        if machineID is not None:
            self._machineID = machineID
        if operatingSystem is not None:
            self._operatingSystem = operatingSystem
        if osImage is not None:
            self._osImage = osImage
        if systemUUID is not None:
            self._systemUUID = systemUUID


class io__k8s__api__core__v1__ObjectFieldSelector(K8STemplatable):
    """ObjectFieldSelector selects an APIVersioned field of an object."""

    props: List[str] = ["apiVersion", "fieldPath"]
    required_props: List[str] = ["fieldPath"]

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @property
    def fieldPath(self) -> str:
        return self._fieldPath

    def __init__(self, fieldPath: str, apiVersion: Optional[str] = None):
        super().__init__()
        if fieldPath is not None:
            self._fieldPath = fieldPath
        if apiVersion is not None:
            self._apiVersion = apiVersion


class io__k8s__api__core__v1__ObjectReference(K8STemplatable):
    """ObjectReference contains enough information to let you inspect or modify the referred object."""

    props: List[str] = [
        "apiVersion",
        "fieldPath",
        "kind",
        "name",
        "namespace",
        "resourceVersion",
        "uid",
    ]
    required_props: List[str] = []

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @property
    def fieldPath(self) -> Optional[str]:
        return self._fieldPath

    @property
    def kind(self) -> Optional[str]:
        return self._kind

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    @property
    def resourceVersion(self) -> Optional[str]:
        return self._resourceVersion

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    def __init__(
        self,
        apiVersion: Optional[str] = None,
        fieldPath: Optional[str] = None,
        kind: Optional[str] = None,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        resourceVersion: Optional[str] = None,
        uid: Optional[str] = None,
    ):
        super().__init__()
        if apiVersion is not None:
            self._apiVersion = apiVersion
        if fieldPath is not None:
            self._fieldPath = fieldPath
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace
        if resourceVersion is not None:
            self._resourceVersion = resourceVersion
        if uid is not None:
            self._uid = uid


class io__k8s__api__core__v1__PersistentVolumeClaimVolumeSource(K8STemplatable):
    """PersistentVolumeClaimVolumeSource references the user's PVC in the same namespace. This volume finds the bound PV and mounts that volume for the pod. A PersistentVolumeClaimVolumeSource is, essentially, a wrapper around another type of volume that is owned by someone else (the system)."""

    props: List[str] = ["claimName", "readOnly"]
    required_props: List[str] = ["claimName"]

    @property
    def claimName(self) -> str:
        return self._claimName

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    def __init__(self, claimName: str, readOnly: Optional[bool] = None):
        super().__init__()
        if claimName is not None:
            self._claimName = claimName
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__PersistentVolumeStatus(K8STemplatable):
    """PersistentVolumeStatus is the current status of a persistent volume."""

    props: List[str] = ["message", "phase", "reason"]
    required_props: List[str] = []

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def phase(
        self,
    ) -> Optional[Literal["Available", "Bound", "Failed", "Pending", "Released"]]:
        return self._phase

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    def __init__(
        self,
        message: Optional[str] = None,
        phase: Optional[
            Literal["Available", "Bound", "Failed", "Pending", "Released"]
        ] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if message is not None:
            self._message = message
        if phase is not None:
            self._phase = phase
        if reason is not None:
            self._reason = reason


class io__k8s__api__core__v1__PhotonPersistentDiskVolumeSource(K8STemplatable):
    """Represents a Photon Controller persistent disk resource."""

    props: List[str] = ["fsType", "pdID"]
    required_props: List[str] = ["pdID"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def pdID(self) -> str:
        return self._pdID

    def __init__(self, pdID: str, fsType: Optional[str] = None):
        super().__init__()
        if pdID is not None:
            self._pdID = pdID
        if fsType is not None:
            self._fsType = fsType


class io__k8s__api__core__v1__PodDNSConfigOption(K8STemplatable):
    """PodDNSConfigOption defines DNS resolver options of a pod."""

    props: List[str] = ["name", "value"]
    required_props: List[str] = []

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def value(self) -> Optional[str]:
        return self._value

    def __init__(self, name: Optional[str] = None, value: Optional[str] = None):
        super().__init__()
        if name is not None:
            self._name = name
        if value is not None:
            self._value = value


class io__k8s__api__core__v1__PodIP(K8STemplatable):
    """IP address information for entries in the (plural) PodIPs field. Each entry includes:
    IP: An IP address allocated to the pod. Routable at least within the cluster."""

    props: List[str] = ["ip"]
    required_props: List[str] = []

    @property
    def ip(self) -> Optional[str]:
        return self._ip

    def __init__(self, ip: Optional[str] = None):
        super().__init__()
        if ip is not None:
            self._ip = ip


class io__k8s__api__core__v1__PodOS(K8STemplatable):
    """PodOS defines the OS parameters of a pod."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__core__v1__PodReadinessGate(K8STemplatable):
    """PodReadinessGate contains the reference to a pod condition"""

    props: List[str] = ["conditionType"]
    required_props: List[str] = ["conditionType"]

    @property
    def conditionType(self) -> str:
        return self._conditionType

    def __init__(self, conditionType: str):
        super().__init__()
        if conditionType is not None:
            self._conditionType = conditionType


class io__k8s__api__core__v1__PortStatus(K8STemplatable):
    """None"""

    props: List[str] = ["error", "port", "protocol"]
    required_props: List[str] = ["port", "protocol"]

    @property
    def error(self) -> Optional[str]:
        return self._error

    @property
    def port(self) -> int:
        return self._port

    @property
    def protocol(self) -> Literal["SCTP", "TCP", "UDP"]:
        return self._protocol

    def __init__(
        self,
        port: int,
        protocol: Literal["SCTP", "TCP", "UDP"],
        error: Optional[str] = None,
    ):
        super().__init__()
        if port is not None:
            self._port = port
        if protocol is not None:
            self._protocol = protocol
        if error is not None:
            self._error = error


class io__k8s__api__core__v1__PortworxVolumeSource(K8STemplatable):
    """PortworxVolumeSource represents a Portworx volume resource."""

    props: List[str] = ["fsType", "readOnly", "volumeID"]
    required_props: List[str] = ["volumeID"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def volumeID(self) -> str:
        return self._volumeID

    def __init__(
        self,
        volumeID: str,
        fsType: Optional[str] = None,
        readOnly: Optional[bool] = None,
    ):
        super().__init__()
        if volumeID is not None:
            self._volumeID = volumeID
        if fsType is not None:
            self._fsType = fsType
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__core__v1__PreferredSchedulingTerm(K8STemplatable):
    """An empty preferred scheduling term matches all objects with implicit weight 0 (i.e. it's a no-op). A null preferred scheduling term matches no objects (i.e. is also a no-op)."""

    props: List[str] = ["preference", "weight"]
    required_props: List[str] = ["weight", "preference"]

    @property
    def preference(self) -> io__k8s__api__core__v1__NodeSelectorTerm:
        return self._preference

    @property
    def weight(self) -> int:
        return self._weight

    def __init__(
        self, preference: io__k8s__api__core__v1__NodeSelectorTerm, weight: int
    ):
        super().__init__()
        if preference is not None:
            self._preference = preference
        if weight is not None:
            self._weight = weight


class io__k8s__api__core__v1__QuobyteVolumeSource(K8STemplatable):
    """Represents a Quobyte mount that lasts the lifetime of a pod. Quobyte volumes do not support ownership management or SELinux relabeling."""

    props: List[str] = ["group", "readOnly", "registry", "tenant", "user", "volume"]
    required_props: List[str] = ["registry", "volume"]

    @property
    def group(self) -> Optional[str]:
        return self._group

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def registry(self) -> str:
        return self._registry

    @property
    def tenant(self) -> Optional[str]:
        return self._tenant

    @property
    def user(self) -> Optional[str]:
        return self._user

    @property
    def volume(self) -> str:
        return self._volume

    def __init__(
        self,
        registry: str,
        volume: str,
        group: Optional[str] = None,
        readOnly: Optional[bool] = None,
        tenant: Optional[str] = None,
        user: Optional[str] = None,
    ):
        super().__init__()
        if registry is not None:
            self._registry = registry
        if volume is not None:
            self._volume = volume
        if group is not None:
            self._group = group
        if readOnly is not None:
            self._readOnly = readOnly
        if tenant is not None:
            self._tenant = tenant
        if user is not None:
            self._user = user


class io__k8s__api__core__v1__RBDVolumeSource(K8STemplatable):
    """Represents a Rados Block Device mount that lasts the lifetime of a pod. RBD volumes support ownership management and SELinux relabeling."""

    props: List[str] = [
        "fsType",
        "image",
        "keyring",
        "monitors",
        "pool",
        "readOnly",
        "secretRef",
        "user",
    ]
    required_props: List[str] = ["monitors", "image"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def image(self) -> str:
        return self._image

    @property
    def keyring(self) -> Optional[str]:
        return self._keyring

    @property
    def monitors(self) -> List[str]:
        return self._monitors

    @property
    def pool(self) -> Optional[str]:
        return self._pool

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__LocalObjectReference]:
        return self._secretRef

    @property
    def user(self) -> Optional[str]:
        return self._user

    def __init__(
        self,
        image: str,
        monitors: List[str],
        fsType: Optional[str] = None,
        keyring: Optional[str] = None,
        pool: Optional[str] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__LocalObjectReference] = None,
        user: Optional[str] = None,
    ):
        super().__init__()
        if image is not None:
            self._image = image
        if monitors is not None:
            self._monitors = monitors
        if fsType is not None:
            self._fsType = fsType
        if keyring is not None:
            self._keyring = keyring
        if pool is not None:
            self._pool = pool
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef
        if user is not None:
            self._user = user


class io__k8s__api__core__v1__SELinuxOptions(K8STemplatable):
    """SELinuxOptions are the labels to be applied to the container"""

    props: List[str] = ["level", "role", "type", "user"]
    required_props: List[str] = []

    @property
    def level(self) -> Optional[str]:
        return self._level

    @property
    def role(self) -> Optional[str]:
        return self._role

    @property
    def type(self) -> Optional[str]:
        return self._type

    @property
    def user(self) -> Optional[str]:
        return self._user

    def __init__(
        self,
        level: Optional[str] = None,
        role: Optional[str] = None,
        type: Optional[str] = None,
        user: Optional[str] = None,
    ):
        super().__init__()
        if level is not None:
            self._level = level
        if role is not None:
            self._role = role
        if type is not None:
            self._type = type
        if user is not None:
            self._user = user


class io__k8s__api__core__v1__ScaleIOVolumeSource(K8STemplatable):
    """ScaleIOVolumeSource represents a persistent ScaleIO volume"""

    props: List[str] = [
        "fsType",
        "gateway",
        "protectionDomain",
        "readOnly",
        "secretRef",
        "sslEnabled",
        "storageMode",
        "storagePool",
        "system",
        "volumeName",
    ]
    required_props: List[str] = ["gateway", "system", "secretRef"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def gateway(self) -> str:
        return self._gateway

    @property
    def protectionDomain(self) -> Optional[str]:
        return self._protectionDomain

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> io__k8s__api__core__v1__LocalObjectReference:
        return self._secretRef

    @property
    def sslEnabled(self) -> Optional[bool]:
        return self._sslEnabled

    @property
    def storageMode(self) -> Optional[str]:
        return self._storageMode

    @property
    def storagePool(self) -> Optional[str]:
        return self._storagePool

    @property
    def system(self) -> str:
        return self._system

    @property
    def volumeName(self) -> Optional[str]:
        return self._volumeName

    def __init__(
        self,
        gateway: str,
        secretRef: io__k8s__api__core__v1__LocalObjectReference,
        system: str,
        fsType: Optional[str] = None,
        protectionDomain: Optional[str] = None,
        readOnly: Optional[bool] = None,
        sslEnabled: Optional[bool] = None,
        storageMode: Optional[str] = None,
        storagePool: Optional[str] = None,
        volumeName: Optional[str] = None,
    ):
        super().__init__()
        if gateway is not None:
            self._gateway = gateway
        if secretRef is not None:
            self._secretRef = secretRef
        if system is not None:
            self._system = system
        if fsType is not None:
            self._fsType = fsType
        if protectionDomain is not None:
            self._protectionDomain = protectionDomain
        if readOnly is not None:
            self._readOnly = readOnly
        if sslEnabled is not None:
            self._sslEnabled = sslEnabled
        if storageMode is not None:
            self._storageMode = storageMode
        if storagePool is not None:
            self._storagePool = storagePool
        if volumeName is not None:
            self._volumeName = volumeName


class io__k8s__api__core__v1__ScopedResourceSelectorRequirement(K8STemplatable):
    """A scoped-resource selector requirement is a selector that contains values, a scope name, and an operator that relates the scope name and values."""

    props: List[str] = ["operator", "scopeName", "values"]
    required_props: List[str] = ["scopeName", "operator"]

    @property
    def operator(self) -> Literal["DoesNotExist", "Exists", "In", "NotIn"]:
        return self._operator

    @property
    def scopeName(
        self,
    ) -> Literal[
        "BestEffort",
        "CrossNamespacePodAffinity",
        "NotBestEffort",
        "NotTerminating",
        "PriorityClass",
        "Terminating",
    ]:
        return self._scopeName

    @property
    def values(self) -> Optional[List[str]]:
        return self._values

    def __init__(
        self,
        operator: Literal["DoesNotExist", "Exists", "In", "NotIn"],
        scopeName: Literal[
            "BestEffort",
            "CrossNamespacePodAffinity",
            "NotBestEffort",
            "NotTerminating",
            "PriorityClass",
            "Terminating",
        ],
        values: Optional[List[str]] = None,
    ):
        super().__init__()
        if operator is not None:
            self._operator = operator
        if scopeName is not None:
            self._scopeName = scopeName
        if values is not None:
            self._values = values


class io__k8s__api__core__v1__SeccompProfile(K8STemplatable):
    """SeccompProfile defines a pod/container's seccomp profile settings. Only one profile source may be set."""

    props: List[str] = ["localhostProfile", "type"]
    required_props: List[str] = ["type"]

    @property
    def localhostProfile(self) -> Optional[str]:
        return self._localhostProfile

    @property
    def type(self) -> Literal["Localhost", "RuntimeDefault", "Unconfined"]:
        return self._type

    def __init__(
        self,
        type: Literal["Localhost", "RuntimeDefault", "Unconfined"],
        localhostProfile: Optional[str] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if localhostProfile is not None:
            self._localhostProfile = localhostProfile


class io__k8s__api__core__v1__SecretEnvSource(K8STemplatable):
    """SecretEnvSource selects a Secret to populate the environment variables with.

    The contents of the target Secret's Data field will represent the key-value pairs as environment variables."""

    props: List[str] = ["name", "optional"]
    required_props: List[str] = []

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def optional(self) -> Optional[bool]:
        return self._optional

    def __init__(self, name: Optional[str] = None, optional: Optional[bool] = None):
        super().__init__()
        if name is not None:
            self._name = name
        if optional is not None:
            self._optional = optional


class io__k8s__api__core__v1__SecretKeySelector(K8STemplatable):
    """SecretKeySelector selects a key of a Secret."""

    props: List[str] = ["key", "name", "optional"]
    required_props: List[str] = ["key"]

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def optional(self) -> Optional[bool]:
        return self._optional

    def __init__(
        self, key: str, name: Optional[str] = None, optional: Optional[bool] = None
    ):
        super().__init__()
        if key is not None:
            self._key = key
        if name is not None:
            self._name = name
        if optional is not None:
            self._optional = optional


class io__k8s__api__core__v1__SecretProjection(K8STemplatable):
    """Adapts a secret into a projected volume.

    The contents of the target Secret's Data field will be presented in a projected volume as files using the keys in the Data field as the file names. Note that this is identical to a secret volume source without the default mode."""

    props: List[str] = ["items", "name", "optional"]
    required_props: List[str] = []

    @property
    def items(self) -> Optional[List[io__k8s__api__core__v1__KeyToPath]]:
        return self._items

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def optional(self) -> Optional[bool]:
        return self._optional

    def __init__(
        self,
        items: Optional[List[io__k8s__api__core__v1__KeyToPath]] = None,
        name: Optional[str] = None,
        optional: Optional[bool] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if name is not None:
            self._name = name
        if optional is not None:
            self._optional = optional


class io__k8s__api__core__v1__SecretReference(K8STemplatable):
    """SecretReference represents a Secret Reference. It has enough information to retrieve secret in any namespace"""

    props: List[str] = ["name", "namespace"]
    required_props: List[str] = []

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    def __init__(self, name: Optional[str] = None, namespace: Optional[str] = None):
        super().__init__()
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace


class io__k8s__api__core__v1__SecretVolumeSource(K8STemplatable):
    """Adapts a Secret into a volume.

    The contents of the target Secret's Data field will be presented in a volume as files using the keys in the Data field as the file names. Secret volumes support ownership management and SELinux relabeling."""

    props: List[str] = ["defaultMode", "items", "optional", "secretName"]
    required_props: List[str] = []

    @property
    def defaultMode(self) -> Optional[int]:
        return self._defaultMode

    @property
    def items(self) -> Optional[List[io__k8s__api__core__v1__KeyToPath]]:
        return self._items

    @property
    def optional(self) -> Optional[bool]:
        return self._optional

    @property
    def secretName(self) -> Optional[str]:
        return self._secretName

    def __init__(
        self,
        defaultMode: Optional[int] = None,
        items: Optional[List[io__k8s__api__core__v1__KeyToPath]] = None,
        optional: Optional[bool] = None,
        secretName: Optional[str] = None,
    ):
        super().__init__()
        if defaultMode is not None:
            self._defaultMode = defaultMode
        if items is not None:
            self._items = items
        if optional is not None:
            self._optional = optional
        if secretName is not None:
            self._secretName = secretName


class io__k8s__api__core__v1__ServiceAccountTokenProjection(K8STemplatable):
    """ServiceAccountTokenProjection represents a projected service account token volume. This projection can be used to insert a service account token into the pods runtime filesystem for use against APIs (Kubernetes API Server or otherwise)."""

    props: List[str] = ["audience", "expirationSeconds", "path"]
    required_props: List[str] = ["path"]

    @property
    def audience(self) -> Optional[str]:
        return self._audience

    @property
    def expirationSeconds(self) -> Optional[int]:
        return self._expirationSeconds

    @property
    def path(self) -> str:
        return self._path

    def __init__(
        self,
        path: str,
        audience: Optional[str] = None,
        expirationSeconds: Optional[int] = None,
    ):
        super().__init__()
        if path is not None:
            self._path = path
        if audience is not None:
            self._audience = audience
        if expirationSeconds is not None:
            self._expirationSeconds = expirationSeconds


class io__k8s__api__core__v1__SessionAffinityConfig(K8STemplatable):
    """SessionAffinityConfig represents the configurations of session affinity."""

    props: List[str] = ["clientIP"]
    required_props: List[str] = []

    @property
    def clientIP(self) -> Optional[io__k8s__api__core__v1__ClientIPConfig]:
        return self._clientIP

    def __init__(
        self, clientIP: Optional[io__k8s__api__core__v1__ClientIPConfig] = None
    ):
        super().__init__()
        if clientIP is not None:
            self._clientIP = clientIP


class io__k8s__api__core__v1__StorageOSPersistentVolumeSource(K8STemplatable):
    """Represents a StorageOS persistent volume resource."""

    props: List[str] = [
        "fsType",
        "readOnly",
        "secretRef",
        "volumeName",
        "volumeNamespace",
    ]
    required_props: List[str] = []

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._secretRef

    @property
    def volumeName(self) -> Optional[str]:
        return self._volumeName

    @property
    def volumeNamespace(self) -> Optional[str]:
        return self._volumeNamespace

    def __init__(
        self,
        fsType: Optional[str] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        volumeName: Optional[str] = None,
        volumeNamespace: Optional[str] = None,
    ):
        super().__init__()
        if fsType is not None:
            self._fsType = fsType
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef
        if volumeName is not None:
            self._volumeName = volumeName
        if volumeNamespace is not None:
            self._volumeNamespace = volumeNamespace


class io__k8s__api__core__v1__StorageOSVolumeSource(K8STemplatable):
    """Represents a StorageOS persistent volume resource."""

    props: List[str] = [
        "fsType",
        "readOnly",
        "secretRef",
        "volumeName",
        "volumeNamespace",
    ]
    required_props: List[str] = []

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__LocalObjectReference]:
        return self._secretRef

    @property
    def volumeName(self) -> Optional[str]:
        return self._volumeName

    @property
    def volumeNamespace(self) -> Optional[str]:
        return self._volumeNamespace

    def __init__(
        self,
        fsType: Optional[str] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__LocalObjectReference] = None,
        volumeName: Optional[str] = None,
        volumeNamespace: Optional[str] = None,
    ):
        super().__init__()
        if fsType is not None:
            self._fsType = fsType
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef
        if volumeName is not None:
            self._volumeName = volumeName
        if volumeNamespace is not None:
            self._volumeNamespace = volumeNamespace


class io__k8s__api__core__v1__Sysctl(K8STemplatable):
    """Sysctl defines a kernel parameter to be set"""

    props: List[str] = ["name", "value"]
    required_props: List[str] = ["name", "value"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    def __init__(self, name: str, value: str):
        super().__init__()
        if name is not None:
            self._name = name
        if value is not None:
            self._value = value


class io__k8s__api__core__v1__Toleration(K8STemplatable):
    """The pod this Toleration is attached to tolerates any taint that matches the triple <key,value,effect> using the matching operator <operator>."""

    props: List[str] = ["effect", "key", "operator", "tolerationSeconds", "value"]
    required_props: List[str] = []

    @property
    def effect(
        self,
    ) -> Optional[Literal["NoExecute", "NoSchedule", "PreferNoSchedule"]]:
        return self._effect

    @property
    def key(self) -> Optional[str]:
        return self._key

    @property
    def operator(self) -> Optional[Literal["Equal", "Exists"]]:
        return self._operator

    @property
    def tolerationSeconds(self) -> Optional[int]:
        return self._tolerationSeconds

    @property
    def value(self) -> Optional[str]:
        return self._value

    def __init__(
        self,
        effect: Optional[Literal["NoExecute", "NoSchedule", "PreferNoSchedule"]] = None,
        key: Optional[str] = None,
        operator: Optional[Literal["Equal", "Exists"]] = None,
        tolerationSeconds: Optional[int] = None,
        value: Optional[str] = None,
    ):
        super().__init__()
        if effect is not None:
            self._effect = effect
        if key is not None:
            self._key = key
        if operator is not None:
            self._operator = operator
        if tolerationSeconds is not None:
            self._tolerationSeconds = tolerationSeconds
        if value is not None:
            self._value = value


class io__k8s__api__core__v1__TopologySelectorLabelRequirement(K8STemplatable):
    """A topology selector requirement is a selector that matches given label. This is an alpha feature and may change in the future."""

    props: List[str] = ["key", "values"]
    required_props: List[str] = ["key", "values"]

    @property
    def key(self) -> str:
        return self._key

    @property
    def values(self) -> List[str]:
        return self._values

    def __init__(self, key: str, values: List[str]):
        super().__init__()
        if key is not None:
            self._key = key
        if values is not None:
            self._values = values


class io__k8s__api__core__v1__TopologySelectorTerm(K8STemplatable):
    """A topology selector term represents the result of label queries. A null or empty topology selector term matches no objects. The requirements of them are ANDed. It provides a subset of functionality as NodeSelectorTerm. This is an alpha feature and may change in the future."""

    props: List[str] = ["matchLabelExpressions"]
    required_props: List[str] = []

    @property
    def matchLabelExpressions(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__TopologySelectorLabelRequirement]]:
        return self._matchLabelExpressions

    def __init__(
        self,
        matchLabelExpressions: Optional[
            List[io__k8s__api__core__v1__TopologySelectorLabelRequirement]
        ] = None,
    ):
        super().__init__()
        if matchLabelExpressions is not None:
            self._matchLabelExpressions = matchLabelExpressions


class io__k8s__api__core__v1__TypedLocalObjectReference(K8STemplatable):
    """TypedLocalObjectReference contains enough information to let you locate the typed referenced object inside the same namespace."""

    props: List[str] = ["apiGroup", "kind", "name"]
    required_props: List[str] = ["kind", "name"]

    @property
    def apiGroup(self) -> Optional[str]:
        return self._apiGroup

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, kind: str, name: str, apiGroup: Optional[str] = None):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if apiGroup is not None:
            self._apiGroup = apiGroup


class io__k8s__api__core__v1__VolumeDevice(K8STemplatable):
    """volumeDevice describes a mapping of a raw block device within a container."""

    props: List[str] = ["devicePath", "name"]
    required_props: List[str] = ["name", "devicePath"]

    @property
    def devicePath(self) -> str:
        return self._devicePath

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, devicePath: str, name: str):
        super().__init__()
        if devicePath is not None:
            self._devicePath = devicePath
        if name is not None:
            self._name = name


class io__k8s__api__core__v1__VolumeMount(K8STemplatable):
    """VolumeMount describes a mounting of a Volume within a container."""

    props: List[str] = [
        "mountPath",
        "mountPropagation",
        "name",
        "readOnly",
        "subPath",
        "subPathExpr",
    ]
    required_props: List[str] = ["name", "mountPath"]

    @property
    def mountPath(self) -> str:
        return self._mountPath

    @property
    def mountPropagation(self) -> Optional[str]:
        return self._mountPropagation

    @property
    def name(self) -> str:
        return self._name

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def subPath(self) -> Optional[str]:
        return self._subPath

    @property
    def subPathExpr(self) -> Optional[str]:
        return self._subPathExpr

    def __init__(
        self,
        mountPath: str,
        name: str,
        mountPropagation: Optional[str] = None,
        readOnly: Optional[bool] = None,
        subPath: Optional[str] = None,
        subPathExpr: Optional[str] = None,
    ):
        super().__init__()
        if mountPath is not None:
            self._mountPath = mountPath
        if name is not None:
            self._name = name
        if mountPropagation is not None:
            self._mountPropagation = mountPropagation
        if readOnly is not None:
            self._readOnly = readOnly
        if subPath is not None:
            self._subPath = subPath
        if subPathExpr is not None:
            self._subPathExpr = subPathExpr


class io__k8s__api__core__v1__VsphereVirtualDiskVolumeSource(K8STemplatable):
    """Represents a vSphere volume resource."""

    props: List[str] = ["fsType", "storagePolicyID", "storagePolicyName", "volumePath"]
    required_props: List[str] = ["volumePath"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def storagePolicyID(self) -> Optional[str]:
        return self._storagePolicyID

    @property
    def storagePolicyName(self) -> Optional[str]:
        return self._storagePolicyName

    @property
    def volumePath(self) -> str:
        return self._volumePath

    def __init__(
        self,
        volumePath: str,
        fsType: Optional[str] = None,
        storagePolicyID: Optional[str] = None,
        storagePolicyName: Optional[str] = None,
    ):
        super().__init__()
        if volumePath is not None:
            self._volumePath = volumePath
        if fsType is not None:
            self._fsType = fsType
        if storagePolicyID is not None:
            self._storagePolicyID = storagePolicyID
        if storagePolicyName is not None:
            self._storagePolicyName = storagePolicyName


class io__k8s__api__core__v1__WindowsSecurityContextOptions(K8STemplatable):
    """WindowsSecurityContextOptions contain Windows-specific options and credentials."""

    props: List[str] = [
        "gmsaCredentialSpec",
        "gmsaCredentialSpecName",
        "hostProcess",
        "runAsUserName",
    ]
    required_props: List[str] = []

    @property
    def gmsaCredentialSpec(self) -> Optional[str]:
        return self._gmsaCredentialSpec

    @property
    def gmsaCredentialSpecName(self) -> Optional[str]:
        return self._gmsaCredentialSpecName

    @property
    def hostProcess(self) -> Optional[bool]:
        return self._hostProcess

    @property
    def runAsUserName(self) -> Optional[str]:
        return self._runAsUserName

    def __init__(
        self,
        gmsaCredentialSpec: Optional[str] = None,
        gmsaCredentialSpecName: Optional[str] = None,
        hostProcess: Optional[bool] = None,
        runAsUserName: Optional[str] = None,
    ):
        super().__init__()
        if gmsaCredentialSpec is not None:
            self._gmsaCredentialSpec = gmsaCredentialSpec
        if gmsaCredentialSpecName is not None:
            self._gmsaCredentialSpecName = gmsaCredentialSpecName
        if hostProcess is not None:
            self._hostProcess = hostProcess
        if runAsUserName is not None:
            self._runAsUserName = runAsUserName


class io__k8s__api__discovery__v1__EndpointConditions(K8STemplatable):
    """EndpointConditions represents the current condition of an endpoint."""

    props: List[str] = ["ready", "serving", "terminating"]
    required_props: List[str] = []

    @property
    def ready(self) -> Optional[bool]:
        return self._ready

    @property
    def serving(self) -> Optional[bool]:
        return self._serving

    @property
    def terminating(self) -> Optional[bool]:
        return self._terminating

    def __init__(
        self,
        ready: Optional[bool] = None,
        serving: Optional[bool] = None,
        terminating: Optional[bool] = None,
    ):
        super().__init__()
        if ready is not None:
            self._ready = ready
        if serving is not None:
            self._serving = serving
        if terminating is not None:
            self._terminating = terminating


class io__k8s__api__discovery__v1__EndpointPort(K8STemplatable):
    """EndpointPort represents a Port used by an EndpointSlice"""

    props: List[str] = ["appProtocol", "name", "port", "protocol"]
    required_props: List[str] = []

    @property
    def appProtocol(self) -> Optional[str]:
        return self._appProtocol

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def port(self) -> Optional[int]:
        return self._port

    @property
    def protocol(self) -> Optional[str]:
        return self._protocol

    def __init__(
        self,
        appProtocol: Optional[str] = None,
        name: Optional[str] = None,
        port: Optional[int] = None,
        protocol: Optional[str] = None,
    ):
        super().__init__()
        if appProtocol is not None:
            self._appProtocol = appProtocol
        if name is not None:
            self._name = name
        if port is not None:
            self._port = port
        if protocol is not None:
            self._protocol = protocol


class io__k8s__api__discovery__v1__ForZone(K8STemplatable):
    """ForZone provides information about which zones should consume this endpoint."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__discovery__v1beta1__EndpointConditions(K8STemplatable):
    """EndpointConditions represents the current condition of an endpoint."""

    props: List[str] = ["ready", "serving", "terminating"]
    required_props: List[str] = []

    @property
    def ready(self) -> Optional[bool]:
        return self._ready

    @property
    def serving(self) -> Optional[bool]:
        return self._serving

    @property
    def terminating(self) -> Optional[bool]:
        return self._terminating

    def __init__(
        self,
        ready: Optional[bool] = None,
        serving: Optional[bool] = None,
        terminating: Optional[bool] = None,
    ):
        super().__init__()
        if ready is not None:
            self._ready = ready
        if serving is not None:
            self._serving = serving
        if terminating is not None:
            self._terminating = terminating


class io__k8s__api__discovery__v1beta1__EndpointPort(K8STemplatable):
    """EndpointPort represents a Port used by an EndpointSlice"""

    props: List[str] = ["appProtocol", "name", "port", "protocol"]
    required_props: List[str] = []

    @property
    def appProtocol(self) -> Optional[str]:
        return self._appProtocol

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def port(self) -> Optional[int]:
        return self._port

    @property
    def protocol(self) -> Optional[str]:
        return self._protocol

    def __init__(
        self,
        appProtocol: Optional[str] = None,
        name: Optional[str] = None,
        port: Optional[int] = None,
        protocol: Optional[str] = None,
    ):
        super().__init__()
        if appProtocol is not None:
            self._appProtocol = appProtocol
        if name is not None:
            self._name = name
        if port is not None:
            self._port = port
        if protocol is not None:
            self._protocol = protocol


class io__k8s__api__discovery__v1beta1__ForZone(K8STemplatable):
    """ForZone provides information about which zones should consume this endpoint."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__flowcontrol__v1beta1__FlowDistinguisherMethod(K8STemplatable):
    """FlowDistinguisherMethod specifies the method of a flow distinguisher."""

    props: List[str] = ["type"]
    required_props: List[str] = ["type"]

    @property
    def type(self) -> str:
        return self._type

    def __init__(self, type: str):
        super().__init__()
        if type is not None:
            self._type = type


class io__k8s__api__flowcontrol__v1beta1__GroupSubject(K8STemplatable):
    """GroupSubject holds detailed information for group-kind subject."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__flowcontrol__v1beta1__NonResourcePolicyRule(K8STemplatable):
    """NonResourcePolicyRule is a predicate that matches non-resource requests according to their verb and the target non-resource URL. A NonResourcePolicyRule matches a request if and only if both (a) at least one member of verbs matches the request and (b) at least one member of nonResourceURLs matches the request."""

    props: List[str] = ["nonResourceURLs", "verbs"]
    required_props: List[str] = ["verbs", "nonResourceURLs"]

    @property
    def nonResourceURLs(self) -> List[str]:
        return self._nonResourceURLs

    @property
    def verbs(self) -> List[str]:
        return self._verbs

    def __init__(self, nonResourceURLs: List[str], verbs: List[str]):
        super().__init__()
        if nonResourceURLs is not None:
            self._nonResourceURLs = nonResourceURLs
        if verbs is not None:
            self._verbs = verbs


class io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationReference(
    K8STemplatable
):
    """PriorityLevelConfigurationReference contains information that points to the "request-priority" being used."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__flowcontrol__v1beta1__QueuingConfiguration(K8STemplatable):
    """QueuingConfiguration holds the configuration parameters for queuing"""

    props: List[str] = ["handSize", "queueLengthLimit", "queues"]
    required_props: List[str] = []

    @property
    def handSize(self) -> Optional[int]:
        return self._handSize

    @property
    def queueLengthLimit(self) -> Optional[int]:
        return self._queueLengthLimit

    @property
    def queues(self) -> Optional[int]:
        return self._queues

    def __init__(
        self,
        handSize: Optional[int] = None,
        queueLengthLimit: Optional[int] = None,
        queues: Optional[int] = None,
    ):
        super().__init__()
        if handSize is not None:
            self._handSize = handSize
        if queueLengthLimit is not None:
            self._queueLengthLimit = queueLengthLimit
        if queues is not None:
            self._queues = queues


class io__k8s__api__flowcontrol__v1beta1__ResourcePolicyRule(K8STemplatable):
    """ResourcePolicyRule is a predicate that matches some resource requests, testing the request's verb and the target resource. A ResourcePolicyRule matches a resource request if and only if: (a) at least one member of verbs matches the request, (b) at least one member of apiGroups matches the request, (c) at least one member of resources matches the request, and (d) either (d1) the request does not specify a namespace (i.e., `Namespace==""`) and clusterScope is true or (d2) the request specifies a namespace and least one member of namespaces matches the request's namespace."""

    props: List[str] = ["apiGroups", "clusterScope", "namespaces", "resources", "verbs"]
    required_props: List[str] = ["verbs", "apiGroups", "resources"]

    @property
    def apiGroups(self) -> List[str]:
        return self._apiGroups

    @property
    def clusterScope(self) -> Optional[bool]:
        return self._clusterScope

    @property
    def namespaces(self) -> Optional[List[str]]:
        return self._namespaces

    @property
    def resources(self) -> List[str]:
        return self._resources

    @property
    def verbs(self) -> List[str]:
        return self._verbs

    def __init__(
        self,
        apiGroups: List[str],
        resources: List[str],
        verbs: List[str],
        clusterScope: Optional[bool] = None,
        namespaces: Optional[List[str]] = None,
    ):
        super().__init__()
        if apiGroups is not None:
            self._apiGroups = apiGroups
        if resources is not None:
            self._resources = resources
        if verbs is not None:
            self._verbs = verbs
        if clusterScope is not None:
            self._clusterScope = clusterScope
        if namespaces is not None:
            self._namespaces = namespaces


class io__k8s__api__flowcontrol__v1beta1__ServiceAccountSubject(K8STemplatable):
    """ServiceAccountSubject holds detailed information for service-account-kind subject."""

    props: List[str] = ["name", "namespace"]
    required_props: List[str] = ["namespace", "name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> str:
        return self._namespace

    def __init__(self, name: str, namespace: str):
        super().__init__()
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace


class io__k8s__api__flowcontrol__v1beta1__UserSubject(K8STemplatable):
    """UserSubject holds detailed information for user-kind subject."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__flowcontrol__v1beta2__FlowDistinguisherMethod(K8STemplatable):
    """FlowDistinguisherMethod specifies the method of a flow distinguisher."""

    props: List[str] = ["type"]
    required_props: List[str] = ["type"]

    @property
    def type(self) -> str:
        return self._type

    def __init__(self, type: str):
        super().__init__()
        if type is not None:
            self._type = type


class io__k8s__api__flowcontrol__v1beta2__GroupSubject(K8STemplatable):
    """GroupSubject holds detailed information for group-kind subject."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__flowcontrol__v1beta2__NonResourcePolicyRule(K8STemplatable):
    """NonResourcePolicyRule is a predicate that matches non-resource requests according to their verb and the target non-resource URL. A NonResourcePolicyRule matches a request if and only if both (a) at least one member of verbs matches the request and (b) at least one member of nonResourceURLs matches the request."""

    props: List[str] = ["nonResourceURLs", "verbs"]
    required_props: List[str] = ["verbs", "nonResourceURLs"]

    @property
    def nonResourceURLs(self) -> List[str]:
        return self._nonResourceURLs

    @property
    def verbs(self) -> List[str]:
        return self._verbs

    def __init__(self, nonResourceURLs: List[str], verbs: List[str]):
        super().__init__()
        if nonResourceURLs is not None:
            self._nonResourceURLs = nonResourceURLs
        if verbs is not None:
            self._verbs = verbs


class io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationReference(
    K8STemplatable
):
    """PriorityLevelConfigurationReference contains information that points to the "request-priority" being used."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__flowcontrol__v1beta2__QueuingConfiguration(K8STemplatable):
    """QueuingConfiguration holds the configuration parameters for queuing"""

    props: List[str] = ["handSize", "queueLengthLimit", "queues"]
    required_props: List[str] = []

    @property
    def handSize(self) -> Optional[int]:
        return self._handSize

    @property
    def queueLengthLimit(self) -> Optional[int]:
        return self._queueLengthLimit

    @property
    def queues(self) -> Optional[int]:
        return self._queues

    def __init__(
        self,
        handSize: Optional[int] = None,
        queueLengthLimit: Optional[int] = None,
        queues: Optional[int] = None,
    ):
        super().__init__()
        if handSize is not None:
            self._handSize = handSize
        if queueLengthLimit is not None:
            self._queueLengthLimit = queueLengthLimit
        if queues is not None:
            self._queues = queues


class io__k8s__api__flowcontrol__v1beta2__ResourcePolicyRule(K8STemplatable):
    """ResourcePolicyRule is a predicate that matches some resource requests, testing the request's verb and the target resource. A ResourcePolicyRule matches a resource request if and only if: (a) at least one member of verbs matches the request, (b) at least one member of apiGroups matches the request, (c) at least one member of resources matches the request, and (d) either (d1) the request does not specify a namespace (i.e., `Namespace==""`) and clusterScope is true or (d2) the request specifies a namespace and least one member of namespaces matches the request's namespace."""

    props: List[str] = ["apiGroups", "clusterScope", "namespaces", "resources", "verbs"]
    required_props: List[str] = ["verbs", "apiGroups", "resources"]

    @property
    def apiGroups(self) -> List[str]:
        return self._apiGroups

    @property
    def clusterScope(self) -> Optional[bool]:
        return self._clusterScope

    @property
    def namespaces(self) -> Optional[List[str]]:
        return self._namespaces

    @property
    def resources(self) -> List[str]:
        return self._resources

    @property
    def verbs(self) -> List[str]:
        return self._verbs

    def __init__(
        self,
        apiGroups: List[str],
        resources: List[str],
        verbs: List[str],
        clusterScope: Optional[bool] = None,
        namespaces: Optional[List[str]] = None,
    ):
        super().__init__()
        if apiGroups is not None:
            self._apiGroups = apiGroups
        if resources is not None:
            self._resources = resources
        if verbs is not None:
            self._verbs = verbs
        if clusterScope is not None:
            self._clusterScope = clusterScope
        if namespaces is not None:
            self._namespaces = namespaces


class io__k8s__api__flowcontrol__v1beta2__ServiceAccountSubject(K8STemplatable):
    """ServiceAccountSubject holds detailed information for service-account-kind subject."""

    props: List[str] = ["name", "namespace"]
    required_props: List[str] = ["namespace", "name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> str:
        return self._namespace

    def __init__(self, name: str, namespace: str):
        super().__init__()
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace


class io__k8s__api__flowcontrol__v1beta2__UserSubject(K8STemplatable):
    """UserSubject holds detailed information for user-kind subject."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__networking__v1__IPBlock(K8STemplatable):
    """IPBlock describes a particular CIDR (Ex. "192.168.1.1/24","2001:db9::/64") that is allowed to the pods matched by a NetworkPolicySpec's podSelector. The except entry describes CIDRs that should not be included within this rule."""

    props: List[str] = ["cidr", "k8s_except"]
    required_props: List[str] = ["cidr"]

    @property
    def cidr(self) -> str:
        return self._cidr

    @property
    def k8s_except(self) -> Optional[List[str]]:
        return self._k8s_except

    def __init__(self, cidr: str, k8s_except: Optional[List[str]] = None):
        super().__init__()
        if cidr is not None:
            self._cidr = cidr
        if k8s_except is not None:
            self._k8s_except = k8s_except


class io__k8s__api__networking__v1__IngressClassParametersReference(K8STemplatable):
    """IngressClassParametersReference identifies an API object. This can be used to specify a cluster or namespace-scoped resource."""

    props: List[str] = ["apiGroup", "kind", "name", "namespace", "scope"]
    required_props: List[str] = ["kind", "name"]

    @property
    def apiGroup(self) -> Optional[str]:
        return self._apiGroup

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    @property
    def scope(self) -> Optional[str]:
        return self._scope

    def __init__(
        self,
        kind: str,
        name: str,
        apiGroup: Optional[str] = None,
        namespace: Optional[str] = None,
        scope: Optional[str] = None,
    ):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if apiGroup is not None:
            self._apiGroup = apiGroup
        if namespace is not None:
            self._namespace = namespace
        if scope is not None:
            self._scope = scope


class io__k8s__api__networking__v1__IngressClassSpec(K8STemplatable):
    """IngressClassSpec provides information about the class of an Ingress."""

    props: List[str] = ["controller", "parameters"]
    required_props: List[str] = []

    @property
    def controller(self) -> Optional[str]:
        return self._controller

    @property
    def parameters(
        self,
    ) -> Optional[io__k8s__api__networking__v1__IngressClassParametersReference]:
        return self._parameters

    def __init__(
        self,
        controller: Optional[str] = None,
        parameters: Optional[
            io__k8s__api__networking__v1__IngressClassParametersReference
        ] = None,
    ):
        super().__init__()
        if controller is not None:
            self._controller = controller
        if parameters is not None:
            self._parameters = parameters


class io__k8s__api__networking__v1__IngressTLS(K8STemplatable):
    """IngressTLS describes the transport layer security associated with an Ingress."""

    props: List[str] = ["hosts", "secretName"]
    required_props: List[str] = []

    @property
    def hosts(self) -> Optional[List[str]]:
        return self._hosts

    @property
    def secretName(self) -> Optional[str]:
        return self._secretName

    def __init__(
        self, hosts: Optional[List[str]] = None, secretName: Optional[str] = None
    ):
        super().__init__()
        if hosts is not None:
            self._hosts = hosts
        if secretName is not None:
            self._secretName = secretName


class io__k8s__api__networking__v1__ServiceBackendPort(K8STemplatable):
    """ServiceBackendPort is the service port being referenced."""

    props: List[str] = ["name", "number"]
    required_props: List[str] = []

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def number(self) -> Optional[int]:
        return self._number

    def __init__(self, name: Optional[str] = None, number: Optional[int] = None):
        super().__init__()
        if name is not None:
            self._name = name
        if number is not None:
            self._number = number


class io__k8s__api__node__v1__Scheduling(K8STemplatable):
    """Scheduling specifies the scheduling constraints for nodes supporting a RuntimeClass."""

    props: List[str] = ["nodeSelector", "tolerations"]
    required_props: List[str] = []

    @property
    def nodeSelector(self) -> Optional[Dict[str, str]]:
        return self._nodeSelector

    @property
    def tolerations(self) -> Optional[List[io__k8s__api__core__v1__Toleration]]:
        return self._tolerations

    def __init__(
        self,
        nodeSelector: Optional[Dict[str, str]] = None,
        tolerations: Optional[List[io__k8s__api__core__v1__Toleration]] = None,
    ):
        super().__init__()
        if nodeSelector is not None:
            self._nodeSelector = nodeSelector
        if tolerations is not None:
            self._tolerations = tolerations


class io__k8s__api__node__v1beta1__Scheduling(K8STemplatable):
    """Scheduling specifies the scheduling constraints for nodes supporting a RuntimeClass."""

    props: List[str] = ["nodeSelector", "tolerations"]
    required_props: List[str] = []

    @property
    def nodeSelector(self) -> Optional[Dict[str, str]]:
        return self._nodeSelector

    @property
    def tolerations(self) -> Optional[List[io__k8s__api__core__v1__Toleration]]:
        return self._tolerations

    def __init__(
        self,
        nodeSelector: Optional[Dict[str, str]] = None,
        tolerations: Optional[List[io__k8s__api__core__v1__Toleration]] = None,
    ):
        super().__init__()
        if nodeSelector is not None:
            self._nodeSelector = nodeSelector
        if tolerations is not None:
            self._tolerations = tolerations


class io__k8s__api__policy__v1beta1__AllowedCSIDriver(K8STemplatable):
    """AllowedCSIDriver represents a single inline CSI Driver that is allowed to be used."""

    props: List[str] = ["name"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()
        if name is not None:
            self._name = name


class io__k8s__api__policy__v1beta1__AllowedFlexVolume(K8STemplatable):
    """AllowedFlexVolume represents a single Flexvolume that is allowed to be used."""

    props: List[str] = ["driver"]
    required_props: List[str] = ["driver"]

    @property
    def driver(self) -> str:
        return self._driver

    def __init__(self, driver: str):
        super().__init__()
        if driver is not None:
            self._driver = driver


class io__k8s__api__policy__v1beta1__AllowedHostPath(K8STemplatable):
    """AllowedHostPath defines the host volume conditions that will be enabled by a policy for pods to use. It requires the path prefix to be defined."""

    props: List[str] = ["pathPrefix", "readOnly"]
    required_props: List[str] = []

    @property
    def pathPrefix(self) -> Optional[str]:
        return self._pathPrefix

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    def __init__(
        self, pathPrefix: Optional[str] = None, readOnly: Optional[bool] = None
    ):
        super().__init__()
        if pathPrefix is not None:
            self._pathPrefix = pathPrefix
        if readOnly is not None:
            self._readOnly = readOnly


class io__k8s__api__policy__v1beta1__HostPortRange(K8STemplatable):
    """HostPortRange defines a range of host ports that will be enabled by a policy for pods to use.  It requires both the start and end to be defined."""

    props: List[str] = ["max", "min"]
    required_props: List[str] = ["min", "max"]

    @property
    def max(self) -> int:
        return self._max

    @property
    def min(self) -> int:
        return self._min

    def __init__(self, max: int, min: int):
        super().__init__()
        if max is not None:
            self._max = max
        if min is not None:
            self._min = min


class io__k8s__api__policy__v1beta1__IDRange(K8STemplatable):
    """IDRange provides a min/max of an allowed range of IDs."""

    props: List[str] = ["max", "min"]
    required_props: List[str] = ["min", "max"]

    @property
    def max(self) -> int:
        return self._max

    @property
    def min(self) -> int:
        return self._min

    def __init__(self, max: int, min: int):
        super().__init__()
        if max is not None:
            self._max = max
        if min is not None:
            self._min = min


class io__k8s__api__policy__v1beta1__RunAsGroupStrategyOptions(K8STemplatable):
    """RunAsGroupStrategyOptions defines the strategy type and any options used to create the strategy."""

    props: List[str] = ["ranges", "rule"]
    required_props: List[str] = ["rule"]

    @property
    def ranges(self) -> Optional[List[io__k8s__api__policy__v1beta1__IDRange]]:
        return self._ranges

    @property
    def rule(self) -> str:
        return self._rule

    def __init__(
        self,
        rule: str,
        ranges: Optional[List[io__k8s__api__policy__v1beta1__IDRange]] = None,
    ):
        super().__init__()
        if rule is not None:
            self._rule = rule
        if ranges is not None:
            self._ranges = ranges


class io__k8s__api__policy__v1beta1__RunAsUserStrategyOptions(K8STemplatable):
    """RunAsUserStrategyOptions defines the strategy type and any options used to create the strategy."""

    props: List[str] = ["ranges", "rule"]
    required_props: List[str] = ["rule"]

    @property
    def ranges(self) -> Optional[List[io__k8s__api__policy__v1beta1__IDRange]]:
        return self._ranges

    @property
    def rule(self) -> str:
        return self._rule

    def __init__(
        self,
        rule: str,
        ranges: Optional[List[io__k8s__api__policy__v1beta1__IDRange]] = None,
    ):
        super().__init__()
        if rule is not None:
            self._rule = rule
        if ranges is not None:
            self._ranges = ranges


class io__k8s__api__policy__v1beta1__RuntimeClassStrategyOptions(K8STemplatable):
    """RuntimeClassStrategyOptions define the strategy that will dictate the allowable RuntimeClasses for a pod."""

    props: List[str] = ["allowedRuntimeClassNames", "defaultRuntimeClassName"]
    required_props: List[str] = ["allowedRuntimeClassNames"]

    @property
    def allowedRuntimeClassNames(self) -> List[str]:
        return self._allowedRuntimeClassNames

    @property
    def defaultRuntimeClassName(self) -> Optional[str]:
        return self._defaultRuntimeClassName

    def __init__(
        self,
        allowedRuntimeClassNames: List[str],
        defaultRuntimeClassName: Optional[str] = None,
    ):
        super().__init__()
        if allowedRuntimeClassNames is not None:
            self._allowedRuntimeClassNames = allowedRuntimeClassNames
        if defaultRuntimeClassName is not None:
            self._defaultRuntimeClassName = defaultRuntimeClassName


class io__k8s__api__policy__v1beta1__SELinuxStrategyOptions(K8STemplatable):
    """SELinuxStrategyOptions defines the strategy type and any options used to create the strategy."""

    props: List[str] = ["rule", "seLinuxOptions"]
    required_props: List[str] = ["rule"]

    @property
    def rule(self) -> str:
        return self._rule

    @property
    def seLinuxOptions(self) -> Optional[io__k8s__api__core__v1__SELinuxOptions]:
        return self._seLinuxOptions

    def __init__(
        self,
        rule: str,
        seLinuxOptions: Optional[io__k8s__api__core__v1__SELinuxOptions] = None,
    ):
        super().__init__()
        if rule is not None:
            self._rule = rule
        if seLinuxOptions is not None:
            self._seLinuxOptions = seLinuxOptions


class io__k8s__api__policy__v1beta1__SupplementalGroupsStrategyOptions(K8STemplatable):
    """SupplementalGroupsStrategyOptions defines the strategy type and options used to create the strategy."""

    props: List[str] = ["ranges", "rule"]
    required_props: List[str] = []

    @property
    def ranges(self) -> Optional[List[io__k8s__api__policy__v1beta1__IDRange]]:
        return self._ranges

    @property
    def rule(self) -> Optional[str]:
        return self._rule

    def __init__(
        self,
        ranges: Optional[List[io__k8s__api__policy__v1beta1__IDRange]] = None,
        rule: Optional[str] = None,
    ):
        super().__init__()
        if ranges is not None:
            self._ranges = ranges
        if rule is not None:
            self._rule = rule


class io__k8s__api__rbac__v1__PolicyRule(K8STemplatable):
    """PolicyRule holds information that describes a policy rule, but does not contain information about who the rule applies to or which namespace the rule applies to."""

    props: List[str] = [
        "apiGroups",
        "nonResourceURLs",
        "resourceNames",
        "resources",
        "verbs",
    ]
    required_props: List[str] = ["verbs"]

    @property
    def apiGroups(self) -> Optional[List[str]]:
        return self._apiGroups

    @property
    def nonResourceURLs(self) -> Optional[List[str]]:
        return self._nonResourceURLs

    @property
    def resourceNames(self) -> Optional[List[str]]:
        return self._resourceNames

    @property
    def resources(self) -> Optional[List[str]]:
        return self._resources

    @property
    def verbs(self) -> List[str]:
        return self._verbs

    def __init__(
        self,
        verbs: List[str],
        apiGroups: Optional[List[str]] = None,
        nonResourceURLs: Optional[List[str]] = None,
        resourceNames: Optional[List[str]] = None,
        resources: Optional[List[str]] = None,
    ):
        super().__init__()
        if verbs is not None:
            self._verbs = verbs
        if apiGroups is not None:
            self._apiGroups = apiGroups
        if nonResourceURLs is not None:
            self._nonResourceURLs = nonResourceURLs
        if resourceNames is not None:
            self._resourceNames = resourceNames
        if resources is not None:
            self._resources = resources


class io__k8s__api__rbac__v1__RoleRef(K8STemplatable):
    """RoleRef contains information that points to the role being used"""

    props: List[str] = ["apiGroup", "kind", "name"]
    required_props: List[str] = ["apiGroup", "kind", "name"]

    @property
    def apiGroup(self) -> str:
        return self._apiGroup

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, apiGroup: str, kind: str, name: str):
        super().__init__()
        if apiGroup is not None:
            self._apiGroup = apiGroup
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name


class io__k8s__api__rbac__v1__Subject(K8STemplatable):
    """Subject contains a reference to the object or user identities a role binding applies to.  This can either hold a direct API object reference, or a value for non-objects such as user and group names."""

    props: List[str] = ["apiGroup", "kind", "name", "namespace"]
    required_props: List[str] = ["kind", "name"]

    @property
    def apiGroup(self) -> Optional[str]:
        return self._apiGroup

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    def __init__(
        self,
        kind: str,
        name: str,
        apiGroup: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if apiGroup is not None:
            self._apiGroup = apiGroup
        if namespace is not None:
            self._namespace = namespace


class io__k8s__api__storage__v1__TokenRequest(K8STemplatable):
    """TokenRequest contains parameters of a service account token."""

    props: List[str] = ["audience", "expirationSeconds"]
    required_props: List[str] = ["audience"]

    @property
    def audience(self) -> str:
        return self._audience

    @property
    def expirationSeconds(self) -> Optional[int]:
        return self._expirationSeconds

    def __init__(self, audience: str, expirationSeconds: Optional[int] = None):
        super().__init__()
        if audience is not None:
            self._audience = audience
        if expirationSeconds is not None:
            self._expirationSeconds = expirationSeconds


class io__k8s__api__storage__v1__VolumeNodeResources(K8STemplatable):
    """VolumeNodeResources is a set of resource limits for scheduling of volumes."""

    props: List[str] = ["count"]
    required_props: List[str] = []

    @property
    def count(self) -> Optional[int]:
        return self._count

    def __init__(self, count: Optional[int] = None):
        super().__init__()
        if count is not None:
            self._count = count


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceColumnDefinition(
    K8STemplatable
):
    """CustomResourceColumnDefinition specifies a column for server side printing."""

    props: List[str] = ["description", "format", "jsonPath", "name", "priority", "type"]
    required_props: List[str] = ["name", "type", "jsonPath"]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def format(self) -> Optional[str]:
        return self._format

    @property
    def jsonPath(self) -> str:
        return self._jsonPath

    @property
    def name(self) -> str:
        return self._name

    @property
    def priority(self) -> Optional[int]:
        return self._priority

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        jsonPath: str,
        name: str,
        type: str,
        description: Optional[str] = None,
        format: Optional[str] = None,
        priority: Optional[int] = None,
    ):
        super().__init__()
        if jsonPath is not None:
            self._jsonPath = jsonPath
        if name is not None:
            self._name = name
        if type is not None:
            self._type = type
        if description is not None:
            self._description = description
        if format is not None:
            self._format = format
        if priority is not None:
            self._priority = priority


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionNames(
    K8STemplatable
):
    """CustomResourceDefinitionNames indicates the names to serve this CustomResourceDefinition"""

    props: List[str] = [
        "categories",
        "kind",
        "listKind",
        "plural",
        "shortNames",
        "singular",
    ]
    required_props: List[str] = ["plural", "kind"]

    @property
    def categories(self) -> Optional[List[str]]:
        return self._categories

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def listKind(self) -> Optional[str]:
        return self._listKind

    @property
    def plural(self) -> str:
        return self._plural

    @property
    def shortNames(self) -> Optional[List[str]]:
        return self._shortNames

    @property
    def singular(self) -> Optional[str]:
        return self._singular

    def __init__(
        self,
        kind: str,
        plural: str,
        categories: Optional[List[str]] = None,
        listKind: Optional[str] = None,
        shortNames: Optional[List[str]] = None,
        singular: Optional[str] = None,
    ):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if plural is not None:
            self._plural = plural
        if categories is not None:
            self._categories = categories
        if listKind is not None:
            self._listKind = listKind
        if shortNames is not None:
            self._shortNames = shortNames
        if singular is not None:
            self._singular = singular


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresourceScale(
    K8STemplatable
):
    """CustomResourceSubresourceScale defines how to serve the scale subresource for CustomResources."""

    props: List[str] = ["labelSelectorPath", "specReplicasPath", "statusReplicasPath"]
    required_props: List[str] = ["specReplicasPath", "statusReplicasPath"]

    @property
    def labelSelectorPath(self) -> Optional[str]:
        return self._labelSelectorPath

    @property
    def specReplicasPath(self) -> str:
        return self._specReplicasPath

    @property
    def statusReplicasPath(self) -> str:
        return self._statusReplicasPath

    def __init__(
        self,
        specReplicasPath: str,
        statusReplicasPath: str,
        labelSelectorPath: Optional[str] = None,
    ):
        super().__init__()
        if specReplicasPath is not None:
            self._specReplicasPath = specReplicasPath
        if statusReplicasPath is not None:
            self._statusReplicasPath = statusReplicasPath
        if labelSelectorPath is not None:
            self._labelSelectorPath = labelSelectorPath


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresourceStatus(
    K8STemplatable
):
    """CustomResourceSubresourceStatus defines how to serve the status subresource for CustomResources. Status is represented by the `.status` JSON path inside of a CustomResource. When set, * exposes a /status subresource for the custom resource * PUT requests to the /status subresource take a custom resource object, and ignore changes to anything except the status stanza * PUT/POST/PATCH requests to the custom resource ignore changes to the status stanza"""

    props: List[str] = []
    required_props: List[str] = []


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresources(
    K8STemplatable
):
    """CustomResourceSubresources defines the status and scale subresources for CustomResources."""

    props: List[str] = ["scale", "status"]
    required_props: List[str] = []

    @property
    def scale(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresourceScale
    ]:
        return self._scale

    @property
    def status(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresourceStatus
    ]:
        return self._status

    def __init__(
        self,
        scale: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresourceScale
        ] = None,
        status: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresourceStatus
        ] = None,
    ):
        super().__init__()
        if scale is not None:
            self._scale = scale
        if status is not None:
            self._status = status


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ExternalDocumentation(
    K8STemplatable
):
    """ExternalDocumentation allows referencing an external resource for extended documentation."""

    props: List[str] = ["description", "url"]
    required_props: List[str] = []

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def url(self) -> Optional[str]:
        return self._url

    def __init__(self, description: Optional[str] = None, url: Optional[str] = None):
        super().__init__()
        if description is not None:
            self._description = description
        if url is not None:
            self._url = url


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSON(
    K8STemplatable
):
    """JSON represents any valid JSON value. These types are supported: bool, int64, float64, string, []interface{}, map[string]interface{} and nil."""

    props: List[str] = []
    required_props: List[str] = []


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrArray(
    K8STemplatable
):
    """JSONSchemaPropsOrArray represents a value that can either be a JSONSchemaProps or an array of JSONSchemaProps. Mainly here for serialization purposes."""

    props: List[str] = []
    required_props: List[str] = []


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrBool(
    K8STemplatable
):
    """JSONSchemaPropsOrBool represents JSONSchemaProps or a boolean value. Defaults to true for the boolean property."""

    props: List[str] = []
    required_props: List[str] = []


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrStringArray(
    K8STemplatable
):
    """JSONSchemaPropsOrStringArray represents a JSONSchemaProps or a string array."""

    props: List[str] = []
    required_props: List[str] = []


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ServiceReference(
    K8STemplatable
):
    """ServiceReference holds a reference to Service.legacy.k8s.io"""

    props: List[str] = ["name", "namespace", "path", "port"]
    required_props: List[str] = ["namespace", "name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def port(self) -> Optional[int]:
        return self._port

    def __init__(
        self,
        name: str,
        namespace: str,
        path: Optional[str] = None,
        port: Optional[int] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace
        if path is not None:
            self._path = path
        if port is not None:
            self._port = port


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ValidationRule(
    K8STemplatable
):
    """ValidationRule describes a validation rule written in the CEL expression language."""

    props: List[str] = ["message", "rule"]
    required_props: List[str] = ["rule"]

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def rule(self) -> str:
        return self._rule

    def __init__(self, rule: str, message: Optional[str] = None):
        super().__init__()
        if rule is not None:
            self._rule = rule
        if message is not None:
            self._message = message


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__WebhookClientConfig(
    K8STemplatable
):
    """WebhookClientConfig contains the information to make a TLS connection with the webhook."""

    props: List[str] = ["caBundle", "service", "url"]
    required_props: List[str] = []

    @property
    def caBundle(self) -> Optional[str]:
        return self._caBundle

    @property
    def service(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ServiceReference
    ]:
        return self._service

    @property
    def url(self) -> Optional[str]:
        return self._url

    def __init__(
        self,
        caBundle: Optional[str] = None,
        service: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ServiceReference
        ] = None,
        url: Optional[str] = None,
    ):
        super().__init__()
        if caBundle is not None:
            self._caBundle = caBundle
        if service is not None:
            self._service = service
        if url is not None:
            self._url = url


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__WebhookConversion(
    K8STemplatable
):
    """WebhookConversion describes how to call a conversion webhook"""

    props: List[str] = ["clientConfig", "conversionReviewVersions"]
    required_props: List[str] = ["conversionReviewVersions"]

    @property
    def clientConfig(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__WebhookClientConfig
    ]:
        return self._clientConfig

    @property
    def conversionReviewVersions(self) -> List[str]:
        return self._conversionReviewVersions

    def __init__(
        self,
        conversionReviewVersions: List[str],
        clientConfig: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__WebhookClientConfig
        ] = None,
    ):
        super().__init__()
        if conversionReviewVersions is not None:
            self._conversionReviewVersions = conversionReviewVersions
        if clientConfig is not None:
            self._clientConfig = clientConfig


io__k8s__apimachinery__pkg__api__resource__Quantity = str


class io__k8s__apimachinery__pkg__apis__meta__v1__APIResource(K8STemplatable):
    """APIResource specifies the name of a resource and whether it is namespaced."""

    props: List[str] = [
        "categories",
        "group",
        "kind",
        "name",
        "namespaced",
        "shortNames",
        "singularName",
        "storageVersionHash",
        "verbs",
        "version",
    ]
    required_props: List[str] = ["name", "singularName", "namespaced", "kind", "verbs"]

    @property
    def categories(self) -> Optional[List[str]]:
        return self._categories

    @property
    def group(self) -> Optional[str]:
        return self._group

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespaced(self) -> bool:
        return self._namespaced

    @property
    def shortNames(self) -> Optional[List[str]]:
        return self._shortNames

    @property
    def singularName(self) -> str:
        return self._singularName

    @property
    def storageVersionHash(self) -> Optional[str]:
        return self._storageVersionHash

    @property
    def verbs(self) -> List[str]:
        return self._verbs

    @property
    def version(self) -> Optional[str]:
        return self._version

    def __init__(
        self,
        kind: str,
        name: str,
        namespaced: bool,
        singularName: str,
        verbs: List[str],
        categories: Optional[List[str]] = None,
        group: Optional[str] = None,
        shortNames: Optional[List[str]] = None,
        storageVersionHash: Optional[str] = None,
        version: Optional[str] = None,
    ):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if namespaced is not None:
            self._namespaced = namespaced
        if singularName is not None:
            self._singularName = singularName
        if verbs is not None:
            self._verbs = verbs
        if categories is not None:
            self._categories = categories
        if group is not None:
            self._group = group
        if shortNames is not None:
            self._shortNames = shortNames
        if storageVersionHash is not None:
            self._storageVersionHash = storageVersionHash
        if version is not None:
            self._version = version


class io__k8s__apimachinery__pkg__apis__meta__v1__APIResourceList(K8STemplatable):
    """APIResourceList is a list of APIResource, it is used to expose the name of the resources supported in a specific group and version, and if the resource is namespaced."""

    apiVersion: str = "v1"
    kind: str = "APIResourceList"

    props: List[str] = ["apiVersion", "groupVersion", "kind", "resources"]
    required_props: List[str] = ["groupVersion", "resources"]

    @property
    def groupVersion(self) -> str:
        return self._groupVersion

    @property
    def resources(
        self,
    ) -> List[io__k8s__apimachinery__pkg__apis__meta__v1__APIResource]:
        return self._resources

    def __init__(
        self,
        groupVersion: str,
        resources: List[io__k8s__apimachinery__pkg__apis__meta__v1__APIResource],
    ):
        super().__init__()
        if groupVersion is not None:
            self._groupVersion = groupVersion
        if resources is not None:
            self._resources = resources


class io__k8s__apimachinery__pkg__apis__meta__v1__FieldsV1(K8STemplatable):
    """FieldsV1 stores a set of fields in a data structure like a Trie, in JSON format.

    Each key is either a '.' representing the field itself, and will always map to an empty set, or a string representing a sub-field or item. The string will follow one of these four formats: 'f:<name>', where <name> is the name of a field in a struct, or key in a map 'v:<value>', where <value> is the exact json formatted value of a list item 'i:<index>', where <index> is position of a item in a list 'k:<keys>', where <keys> is a map of  a list item's key fields to their unique values If a key maps to an empty Fields value, the field that key represents is part of the set.

    The exact format is defined in sigs.k8s.io/structured-merge-diff"""

    props: List[str] = []
    required_props: List[str] = []


class io__k8s__apimachinery__pkg__apis__meta__v1__GroupVersionForDiscovery(
    K8STemplatable
):
    """GroupVersion contains the "group/version" and "version" string of a version. It is made a struct to keep extensibility."""

    props: List[str] = ["groupVersion", "version"]
    required_props: List[str] = ["groupVersion", "version"]

    @property
    def groupVersion(self) -> str:
        return self._groupVersion

    @property
    def version(self) -> str:
        return self._version

    def __init__(self, groupVersion: str, version: str):
        super().__init__()
        if groupVersion is not None:
            self._groupVersion = groupVersion
        if version is not None:
            self._version = version


class io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelectorRequirement(
    K8STemplatable
):
    """A label selector requirement is a selector that contains values, a key, and an operator that relates the key and values."""

    props: List[str] = ["key", "operator", "values"]
    required_props: List[str] = ["key", "operator"]

    @property
    def key(self) -> str:
        return self._key

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def values(self) -> Optional[List[str]]:
        return self._values

    def __init__(self, key: str, operator: str, values: Optional[List[str]] = None):
        super().__init__()
        if key is not None:
            self._key = key
        if operator is not None:
            self._operator = operator
        if values is not None:
            self._values = values


class io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta(K8STemplatable):
    """ListMeta describes metadata that synthetic resources must have, including lists and various status objects. A resource may have only one of {ObjectMeta, ListMeta}."""

    props: List[str] = [
        "k8s_continue",
        "remainingItemCount",
        "resourceVersion",
        "selfLink",
    ]
    required_props: List[str] = []

    @property
    def k8s_continue(self) -> Optional[str]:
        return self._k8s_continue

    @property
    def remainingItemCount(self) -> Optional[int]:
        return self._remainingItemCount

    @property
    def resourceVersion(self) -> Optional[str]:
        return self._resourceVersion

    @property
    def selfLink(self) -> Optional[str]:
        return self._selfLink

    def __init__(
        self,
        k8s_continue: Optional[str] = None,
        remainingItemCount: Optional[int] = None,
        resourceVersion: Optional[str] = None,
        selfLink: Optional[str] = None,
    ):
        super().__init__()
        if k8s_continue is not None:
            self._k8s_continue = k8s_continue
        if remainingItemCount is not None:
            self._remainingItemCount = remainingItemCount
        if resourceVersion is not None:
            self._resourceVersion = resourceVersion
        if selfLink is not None:
            self._selfLink = selfLink


io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime = str


class io__k8s__apimachinery__pkg__apis__meta__v1__OwnerReference(K8STemplatable):
    """OwnerReference contains enough information to let you identify an owning object. An owning object must be in the same namespace as the dependent, or be cluster-scoped, so there is no namespace field."""

    props: List[str] = [
        "apiVersion",
        "blockOwnerDeletion",
        "controller",
        "kind",
        "name",
        "uid",
    ]
    required_props: List[str] = ["apiVersion", "kind", "name", "uid"]

    @property
    def apiVersion(self) -> str:
        return self._apiVersion

    @property
    def blockOwnerDeletion(self) -> Optional[bool]:
        return self._blockOwnerDeletion

    @property
    def controller(self) -> Optional[bool]:
        return self._controller

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    @property
    def uid(self) -> str:
        return self._uid

    def __init__(
        self,
        apiVersion: str,
        kind: str,
        name: str,
        uid: str,
        blockOwnerDeletion: Optional[bool] = None,
        controller: Optional[bool] = None,
    ):
        super().__init__()
        if apiVersion is not None:
            self._apiVersion = apiVersion
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if uid is not None:
            self._uid = uid
        if blockOwnerDeletion is not None:
            self._blockOwnerDeletion = blockOwnerDeletion
        if controller is not None:
            self._controller = controller


class io__k8s__apimachinery__pkg__apis__meta__v1__Patch(K8STemplatable):
    """Patch is provided to give a concrete name and type to the Kubernetes PATCH request body."""

    props: List[str] = []
    required_props: List[str] = []


class io__k8s__apimachinery__pkg__apis__meta__v1__Preconditions(K8STemplatable):
    """Preconditions must be fulfilled before an operation (update, delete, etc.) is carried out."""

    props: List[str] = ["resourceVersion", "uid"]
    required_props: List[str] = []

    @property
    def resourceVersion(self) -> Optional[str]:
        return self._resourceVersion

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    def __init__(
        self, resourceVersion: Optional[str] = None, uid: Optional[str] = None
    ):
        super().__init__()
        if resourceVersion is not None:
            self._resourceVersion = resourceVersion
        if uid is not None:
            self._uid = uid


class io__k8s__apimachinery__pkg__apis__meta__v1__ServerAddressByClientCIDR(
    K8STemplatable
):
    """ServerAddressByClientCIDR helps the client to determine the server address that they should use, depending on the clientCIDR that they match."""

    props: List[str] = ["clientCIDR", "serverAddress"]
    required_props: List[str] = ["clientCIDR", "serverAddress"]

    @property
    def clientCIDR(self) -> str:
        return self._clientCIDR

    @property
    def serverAddress(self) -> str:
        return self._serverAddress

    def __init__(self, clientCIDR: str, serverAddress: str):
        super().__init__()
        if clientCIDR is not None:
            self._clientCIDR = clientCIDR
        if serverAddress is not None:
            self._serverAddress = serverAddress


class io__k8s__apimachinery__pkg__apis__meta__v1__StatusCause(K8STemplatable):
    """StatusCause provides more information about an api.Status failure, including cases when multiple errors are encountered."""

    props: List[str] = ["field", "message", "reason"]
    required_props: List[str] = []

    @property
    def field(self) -> Optional[str]:
        return self._field

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    def __init__(
        self,
        field: Optional[str] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if field is not None:
            self._field = field
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__apimachinery__pkg__apis__meta__v1__StatusDetails(K8STemplatable):
    """StatusDetails is a set of additional properties that MAY be set by the server to provide additional information about a response. The Reason field of a Status object defines what attributes will be set. Clients must ignore fields that do not match the defined type of each attribute, and should assume that any attribute may be empty, invalid, or under defined."""

    props: List[str] = ["causes", "group", "kind", "name", "retryAfterSeconds", "uid"]
    required_props: List[str] = []

    @property
    def causes(
        self,
    ) -> Optional[List[io__k8s__apimachinery__pkg__apis__meta__v1__StatusCause]]:
        return self._causes

    @property
    def group(self) -> Optional[str]:
        return self._group

    @property
    def kind(self) -> Optional[str]:
        return self._kind

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def retryAfterSeconds(self) -> Optional[int]:
        return self._retryAfterSeconds

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    def __init__(
        self,
        causes: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__StatusCause]
        ] = None,
        group: Optional[str] = None,
        kind: Optional[str] = None,
        name: Optional[str] = None,
        retryAfterSeconds: Optional[int] = None,
        uid: Optional[str] = None,
    ):
        super().__init__()
        if causes is not None:
            self._causes = causes
        if group is not None:
            self._group = group
        if kind is not None:
            self._kind = kind
        if name is not None:
            self._name = name
        if retryAfterSeconds is not None:
            self._retryAfterSeconds = retryAfterSeconds
        if uid is not None:
            self._uid = uid


io__k8s__apimachinery__pkg__apis__meta__v1__Time = str


class io__k8s__apimachinery__pkg__runtime__RawExtension(K8STemplatable):
    """RawExtension is used to hold extensions in external versions.

    To use this, make a field which has RawExtension as its type in your external, versioned struct, and Object in your internal struct. You also need to register your various plugin types.

    // Internal package: type MyAPIObject struct {
            runtime.TypeMeta `json:",inline"`
            MyPlugin runtime.Object `json:"myPlugin"`
    } type PluginA struct {
            AOption string `json:"aOption"`
    }

    // External package: type MyAPIObject struct {
            runtime.TypeMeta `json:",inline"`
            MyPlugin runtime.RawExtension `json:"myPlugin"`
    } type PluginA struct {
            AOption string `json:"aOption"`
    }

    // On the wire, the JSON will look something like this: {
            "kind":"MyAPIObject",
            "apiVersion":"v1",
            "myPlugin": {
                    "kind":"PluginA",
                    "aOption":"foo",
            },
    }

    So what happens? Decode first uses json or yaml to unmarshal the serialized data into your external MyAPIObject. That causes the raw JSON to be stored, but not unpacked. The next step is to copy (using pkg/conversion) into the internal struct. The runtime package's DefaultScheme has conversion functions installed which will unpack the JSON stored in RawExtension, turning it into the correct object type, and storing it in the Object. (TODO: In the case where the object is of an unknown type, a runtime.Unknown object will be created and stored.)"""

    props: List[str] = []
    required_props: List[str] = []


io__k8s__apimachinery__pkg__util__intstr__IntOrString = str


class io__k8s__apimachinery__pkg__version__Info(K8STemplatable):
    """Info contains versioning information. how we'll want to distribute that information."""

    props: List[str] = [
        "buildDate",
        "compiler",
        "gitCommit",
        "gitTreeState",
        "gitVersion",
        "goVersion",
        "major",
        "minor",
        "platform",
    ]
    required_props: List[str] = [
        "major",
        "minor",
        "gitVersion",
        "gitCommit",
        "gitTreeState",
        "buildDate",
        "goVersion",
        "compiler",
        "platform",
    ]

    @property
    def buildDate(self) -> str:
        return self._buildDate

    @property
    def compiler(self) -> str:
        return self._compiler

    @property
    def gitCommit(self) -> str:
        return self._gitCommit

    @property
    def gitTreeState(self) -> str:
        return self._gitTreeState

    @property
    def gitVersion(self) -> str:
        return self._gitVersion

    @property
    def goVersion(self) -> str:
        return self._goVersion

    @property
    def major(self) -> str:
        return self._major

    @property
    def minor(self) -> str:
        return self._minor

    @property
    def platform(self) -> str:
        return self._platform

    def __init__(
        self,
        buildDate: str,
        compiler: str,
        gitCommit: str,
        gitTreeState: str,
        gitVersion: str,
        goVersion: str,
        major: str,
        minor: str,
        platform: str,
    ):
        super().__init__()
        if buildDate is not None:
            self._buildDate = buildDate
        if compiler is not None:
            self._compiler = compiler
        if gitCommit is not None:
            self._gitCommit = gitCommit
        if gitTreeState is not None:
            self._gitTreeState = gitTreeState
        if gitVersion is not None:
            self._gitVersion = gitVersion
        if goVersion is not None:
            self._goVersion = goVersion
        if major is not None:
            self._major = major
        if minor is not None:
            self._minor = minor
        if platform is not None:
            self._platform = platform


class io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceCondition(
    K8STemplatable
):
    """APIServiceCondition describes the state of an APIService at a particular point"""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceStatus(
    K8STemplatable
):
    """APIServiceStatus contains derived information about an API server"""

    props: List[str] = ["conditions"]
    required_props: List[str] = []

    @property
    def conditions(
        self,
    ) -> Optional[
        List[
            io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceCondition
        ]
    ]:
        return self._conditions

    def __init__(
        self,
        conditions: Optional[
            List[
                io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceCondition
            ]
        ] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions


class io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__ServiceReference(
    K8STemplatable
):
    """ServiceReference holds a reference to Service.legacy.k8s.io"""

    props: List[str] = ["name", "namespace", "port"]
    required_props: List[str] = []

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    @property
    def port(self) -> Optional[int]:
        return self._port

    def __init__(
        self,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        port: Optional[int] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace
        if port is not None:
            self._port = port


class io__k8s__api__apiserverinternal__v1alpha1__StorageVersionCondition(
    K8STemplatable
):
    """Describes the state of the storageVersion at a certain point."""

    props: List[str] = [
        "lastTransitionTime",
        "message",
        "observedGeneration",
        "reason",
        "status",
        "type",
    ]
    required_props: List[str] = ["type", "status", "reason"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        reason: str,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        observedGeneration: Optional[int] = None,
    ):
        super().__init__()
        if reason is not None:
            self._reason = reason
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration


class io__k8s__api__apiserverinternal__v1alpha1__StorageVersionStatus(K8STemplatable):
    """API server instances report the versions they can decode and the version they encode objects to when persisting objects in the backend."""

    props: List[str] = ["commonEncodingVersion", "conditions", "storageVersions"]
    required_props: List[str] = []

    @property
    def commonEncodingVersion(self) -> Optional[str]:
        return self._commonEncodingVersion

    @property
    def conditions(
        self,
    ) -> Optional[
        List[io__k8s__api__apiserverinternal__v1alpha1__StorageVersionCondition]
    ]:
        return self._conditions

    @property
    def storageVersions(
        self,
    ) -> Optional[
        List[io__k8s__api__apiserverinternal__v1alpha1__ServerStorageVersion]
    ]:
        return self._storageVersions

    def __init__(
        self,
        commonEncodingVersion: Optional[str] = None,
        conditions: Optional[
            List[io__k8s__api__apiserverinternal__v1alpha1__StorageVersionCondition]
        ] = None,
        storageVersions: Optional[
            List[io__k8s__api__apiserverinternal__v1alpha1__ServerStorageVersion]
        ] = None,
    ):
        super().__init__()
        if commonEncodingVersion is not None:
            self._commonEncodingVersion = commonEncodingVersion
        if conditions is not None:
            self._conditions = conditions
        if storageVersions is not None:
            self._storageVersions = storageVersions


class io__k8s__api__apps__v1__DaemonSetCondition(K8STemplatable):
    """DaemonSetCondition describes the state of a DaemonSet at a certain point."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__apps__v1__DaemonSetStatus(K8STemplatable):
    """DaemonSetStatus represents the current status of a daemon set."""

    props: List[str] = [
        "collisionCount",
        "conditions",
        "currentNumberScheduled",
        "desiredNumberScheduled",
        "numberAvailable",
        "numberMisscheduled",
        "numberReady",
        "numberUnavailable",
        "observedGeneration",
        "updatedNumberScheduled",
    ]
    required_props: List[str] = [
        "currentNumberScheduled",
        "numberMisscheduled",
        "desiredNumberScheduled",
        "numberReady",
    ]

    @property
    def collisionCount(self) -> Optional[int]:
        return self._collisionCount

    @property
    def conditions(self) -> Optional[List[io__k8s__api__apps__v1__DaemonSetCondition]]:
        return self._conditions

    @property
    def currentNumberScheduled(self) -> int:
        return self._currentNumberScheduled

    @property
    def desiredNumberScheduled(self) -> int:
        return self._desiredNumberScheduled

    @property
    def numberAvailable(self) -> Optional[int]:
        return self._numberAvailable

    @property
    def numberMisscheduled(self) -> int:
        return self._numberMisscheduled

    @property
    def numberReady(self) -> int:
        return self._numberReady

    @property
    def numberUnavailable(self) -> Optional[int]:
        return self._numberUnavailable

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    @property
    def updatedNumberScheduled(self) -> Optional[int]:
        return self._updatedNumberScheduled

    def __init__(
        self,
        currentNumberScheduled: int,
        desiredNumberScheduled: int,
        numberMisscheduled: int,
        numberReady: int,
        collisionCount: Optional[int] = None,
        conditions: Optional[List[io__k8s__api__apps__v1__DaemonSetCondition]] = None,
        numberAvailable: Optional[int] = None,
        numberUnavailable: Optional[int] = None,
        observedGeneration: Optional[int] = None,
        updatedNumberScheduled: Optional[int] = None,
    ):
        super().__init__()
        if currentNumberScheduled is not None:
            self._currentNumberScheduled = currentNumberScheduled
        if desiredNumberScheduled is not None:
            self._desiredNumberScheduled = desiredNumberScheduled
        if numberMisscheduled is not None:
            self._numberMisscheduled = numberMisscheduled
        if numberReady is not None:
            self._numberReady = numberReady
        if collisionCount is not None:
            self._collisionCount = collisionCount
        if conditions is not None:
            self._conditions = conditions
        if numberAvailable is not None:
            self._numberAvailable = numberAvailable
        if numberUnavailable is not None:
            self._numberUnavailable = numberUnavailable
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration
        if updatedNumberScheduled is not None:
            self._updatedNumberScheduled = updatedNumberScheduled


class io__k8s__api__apps__v1__DeploymentCondition(K8STemplatable):
    """DeploymentCondition describes the state of a deployment at a certain point."""

    props: List[str] = [
        "lastTransitionTime",
        "lastUpdateTime",
        "message",
        "reason",
        "status",
        "type",
    ]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def lastUpdateTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastUpdateTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastUpdateTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if lastUpdateTime is not None:
            self._lastUpdateTime = lastUpdateTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__apps__v1__DeploymentStatus(K8STemplatable):
    """DeploymentStatus is the most recently observed status of the Deployment."""

    props: List[str] = [
        "availableReplicas",
        "collisionCount",
        "conditions",
        "observedGeneration",
        "readyReplicas",
        "replicas",
        "unavailableReplicas",
        "updatedReplicas",
    ]
    required_props: List[str] = []

    @property
    def availableReplicas(self) -> Optional[int]:
        return self._availableReplicas

    @property
    def collisionCount(self) -> Optional[int]:
        return self._collisionCount

    @property
    def conditions(self) -> Optional[List[io__k8s__api__apps__v1__DeploymentCondition]]:
        return self._conditions

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    @property
    def readyReplicas(self) -> Optional[int]:
        return self._readyReplicas

    @property
    def replicas(self) -> Optional[int]:
        return self._replicas

    @property
    def unavailableReplicas(self) -> Optional[int]:
        return self._unavailableReplicas

    @property
    def updatedReplicas(self) -> Optional[int]:
        return self._updatedReplicas

    def __init__(
        self,
        availableReplicas: Optional[int] = None,
        collisionCount: Optional[int] = None,
        conditions: Optional[List[io__k8s__api__apps__v1__DeploymentCondition]] = None,
        observedGeneration: Optional[int] = None,
        readyReplicas: Optional[int] = None,
        replicas: Optional[int] = None,
        unavailableReplicas: Optional[int] = None,
        updatedReplicas: Optional[int] = None,
    ):
        super().__init__()
        if availableReplicas is not None:
            self._availableReplicas = availableReplicas
        if collisionCount is not None:
            self._collisionCount = collisionCount
        if conditions is not None:
            self._conditions = conditions
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration
        if readyReplicas is not None:
            self._readyReplicas = readyReplicas
        if replicas is not None:
            self._replicas = replicas
        if unavailableReplicas is not None:
            self._unavailableReplicas = unavailableReplicas
        if updatedReplicas is not None:
            self._updatedReplicas = updatedReplicas


class io__k8s__api__apps__v1__ReplicaSetCondition(K8STemplatable):
    """ReplicaSetCondition describes the state of a replica set at a certain point."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__apps__v1__ReplicaSetStatus(K8STemplatable):
    """ReplicaSetStatus represents the current status of a ReplicaSet."""

    props: List[str] = [
        "availableReplicas",
        "conditions",
        "fullyLabeledReplicas",
        "observedGeneration",
        "readyReplicas",
        "replicas",
    ]
    required_props: List[str] = ["replicas"]

    @property
    def availableReplicas(self) -> Optional[int]:
        return self._availableReplicas

    @property
    def conditions(self) -> Optional[List[io__k8s__api__apps__v1__ReplicaSetCondition]]:
        return self._conditions

    @property
    def fullyLabeledReplicas(self) -> Optional[int]:
        return self._fullyLabeledReplicas

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    @property
    def readyReplicas(self) -> Optional[int]:
        return self._readyReplicas

    @property
    def replicas(self) -> int:
        return self._replicas

    def __init__(
        self,
        replicas: int,
        availableReplicas: Optional[int] = None,
        conditions: Optional[List[io__k8s__api__apps__v1__ReplicaSetCondition]] = None,
        fullyLabeledReplicas: Optional[int] = None,
        observedGeneration: Optional[int] = None,
        readyReplicas: Optional[int] = None,
    ):
        super().__init__()
        if replicas is not None:
            self._replicas = replicas
        if availableReplicas is not None:
            self._availableReplicas = availableReplicas
        if conditions is not None:
            self._conditions = conditions
        if fullyLabeledReplicas is not None:
            self._fullyLabeledReplicas = fullyLabeledReplicas
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration
        if readyReplicas is not None:
            self._readyReplicas = readyReplicas


class io__k8s__api__apps__v1__RollingUpdateDaemonSet(K8STemplatable):
    """Spec to control the desired behavior of daemon set rolling update."""

    props: List[str] = ["maxSurge", "maxUnavailable"]
    required_props: List[str] = []

    @property
    def maxSurge(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._maxSurge

    @property
    def maxUnavailable(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._maxUnavailable

    def __init__(
        self,
        maxSurge: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
        maxUnavailable: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
    ):
        super().__init__()
        if maxSurge is not None:
            self._maxSurge = maxSurge
        if maxUnavailable is not None:
            self._maxUnavailable = maxUnavailable


class io__k8s__api__apps__v1__RollingUpdateDeployment(K8STemplatable):
    """Spec to control the desired behavior of rolling update."""

    props: List[str] = ["maxSurge", "maxUnavailable"]
    required_props: List[str] = []

    @property
    def maxSurge(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._maxSurge

    @property
    def maxUnavailable(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._maxUnavailable

    def __init__(
        self,
        maxSurge: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
        maxUnavailable: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
    ):
        super().__init__()
        if maxSurge is not None:
            self._maxSurge = maxSurge
        if maxUnavailable is not None:
            self._maxUnavailable = maxUnavailable


class io__k8s__api__apps__v1__StatefulSetCondition(K8STemplatable):
    """StatefulSetCondition describes the state of a statefulset at a certain point."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__apps__v1__StatefulSetStatus(K8STemplatable):
    """StatefulSetStatus represents the current state of a StatefulSet."""

    props: List[str] = [
        "availableReplicas",
        "collisionCount",
        "conditions",
        "currentReplicas",
        "currentRevision",
        "observedGeneration",
        "readyReplicas",
        "replicas",
        "updateRevision",
        "updatedReplicas",
    ]
    required_props: List[str] = ["replicas", "availableReplicas"]

    @property
    def availableReplicas(self) -> int:
        return self._availableReplicas

    @property
    def collisionCount(self) -> Optional[int]:
        return self._collisionCount

    @property
    def conditions(
        self,
    ) -> Optional[List[io__k8s__api__apps__v1__StatefulSetCondition]]:
        return self._conditions

    @property
    def currentReplicas(self) -> Optional[int]:
        return self._currentReplicas

    @property
    def currentRevision(self) -> Optional[str]:
        return self._currentRevision

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    @property
    def readyReplicas(self) -> Optional[int]:
        return self._readyReplicas

    @property
    def replicas(self) -> int:
        return self._replicas

    @property
    def updateRevision(self) -> Optional[str]:
        return self._updateRevision

    @property
    def updatedReplicas(self) -> Optional[int]:
        return self._updatedReplicas

    def __init__(
        self,
        availableReplicas: int,
        replicas: int,
        collisionCount: Optional[int] = None,
        conditions: Optional[List[io__k8s__api__apps__v1__StatefulSetCondition]] = None,
        currentReplicas: Optional[int] = None,
        currentRevision: Optional[str] = None,
        observedGeneration: Optional[int] = None,
        readyReplicas: Optional[int] = None,
        updateRevision: Optional[str] = None,
        updatedReplicas: Optional[int] = None,
    ):
        super().__init__()
        if availableReplicas is not None:
            self._availableReplicas = availableReplicas
        if replicas is not None:
            self._replicas = replicas
        if collisionCount is not None:
            self._collisionCount = collisionCount
        if conditions is not None:
            self._conditions = conditions
        if currentReplicas is not None:
            self._currentReplicas = currentReplicas
        if currentRevision is not None:
            self._currentRevision = currentRevision
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration
        if readyReplicas is not None:
            self._readyReplicas = readyReplicas
        if updateRevision is not None:
            self._updateRevision = updateRevision
        if updatedReplicas is not None:
            self._updatedReplicas = updatedReplicas


class io__k8s__api__authentication__v1__TokenRequestStatus(K8STemplatable):
    """TokenRequestStatus is the result of a token request."""

    props: List[str] = ["expirationTimestamp", "token"]
    required_props: List[str] = ["token", "expirationTimestamp"]

    @property
    def expirationTimestamp(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__Time:
        return self._expirationTimestamp

    @property
    def token(self) -> str:
        return self._token

    def __init__(
        self,
        expirationTimestamp: io__k8s__apimachinery__pkg__apis__meta__v1__Time,
        token: str,
    ):
        super().__init__()
        if expirationTimestamp is not None:
            self._expirationTimestamp = expirationTimestamp
        if token is not None:
            self._token = token


class io__k8s__api__authentication__v1__TokenReviewStatus(K8STemplatable):
    """TokenReviewStatus is the result of the token authentication request."""

    props: List[str] = ["audiences", "authenticated", "error", "user"]
    required_props: List[str] = []

    @property
    def audiences(self) -> Optional[List[str]]:
        return self._audiences

    @property
    def authenticated(self) -> Optional[bool]:
        return self._authenticated

    @property
    def error(self) -> Optional[str]:
        return self._error

    @property
    def user(self) -> Optional[io__k8s__api__authentication__v1__UserInfo]:
        return self._user

    def __init__(
        self,
        audiences: Optional[List[str]] = None,
        authenticated: Optional[bool] = None,
        error: Optional[str] = None,
        user: Optional[io__k8s__api__authentication__v1__UserInfo] = None,
    ):
        super().__init__()
        if audiences is not None:
            self._audiences = audiences
        if authenticated is not None:
            self._authenticated = authenticated
        if error is not None:
            self._error = error
        if user is not None:
            self._user = user


class io__k8s__api__autoscaling__v1__HorizontalPodAutoscalerStatus(K8STemplatable):
    """current status of a horizontal pod autoscaler"""

    props: List[str] = [
        "currentCPUUtilizationPercentage",
        "currentReplicas",
        "desiredReplicas",
        "lastScaleTime",
        "observedGeneration",
    ]
    required_props: List[str] = ["currentReplicas", "desiredReplicas"]

    @property
    def currentCPUUtilizationPercentage(self) -> Optional[int]:
        return self._currentCPUUtilizationPercentage

    @property
    def currentReplicas(self) -> int:
        return self._currentReplicas

    @property
    def desiredReplicas(self) -> int:
        return self._desiredReplicas

    @property
    def lastScaleTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastScaleTime

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    def __init__(
        self,
        currentReplicas: int,
        desiredReplicas: int,
        currentCPUUtilizationPercentage: Optional[int] = None,
        lastScaleTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        observedGeneration: Optional[int] = None,
    ):
        super().__init__()
        if currentReplicas is not None:
            self._currentReplicas = currentReplicas
        if desiredReplicas is not None:
            self._desiredReplicas = desiredReplicas
        if currentCPUUtilizationPercentage is not None:
            self._currentCPUUtilizationPercentage = currentCPUUtilizationPercentage
        if lastScaleTime is not None:
            self._lastScaleTime = lastScaleTime
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration


class io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerCondition(K8STemplatable):
    """HorizontalPodAutoscalerCondition describes the state of a HorizontalPodAutoscaler at a certain point."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__autoscaling__v2__MetricTarget(K8STemplatable):
    """MetricTarget defines the target value, average value, or average utilization of a specific metric"""

    props: List[str] = ["averageUtilization", "averageValue", "type", "value"]
    required_props: List[str] = ["type"]

    @property
    def averageUtilization(self) -> Optional[int]:
        return self._averageUtilization

    @property
    def averageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._averageValue

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._value

    def __init__(
        self,
        type: str,
        averageUtilization: Optional[int] = None,
        averageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        value: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if averageUtilization is not None:
            self._averageUtilization = averageUtilization
        if averageValue is not None:
            self._averageValue = averageValue
        if value is not None:
            self._value = value


class io__k8s__api__autoscaling__v2__MetricValueStatus(K8STemplatable):
    """MetricValueStatus holds the current value for a metric"""

    props: List[str] = ["averageUtilization", "averageValue", "value"]
    required_props: List[str] = []

    @property
    def averageUtilization(self) -> Optional[int]:
        return self._averageUtilization

    @property
    def averageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._averageValue

    @property
    def value(self) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._value

    def __init__(
        self,
        averageUtilization: Optional[int] = None,
        averageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        value: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
    ):
        super().__init__()
        if averageUtilization is not None:
            self._averageUtilization = averageUtilization
        if averageValue is not None:
            self._averageValue = averageValue
        if value is not None:
            self._value = value


class io__k8s__api__autoscaling__v2__ResourceMetricSource(K8STemplatable):
    """ResourceMetricSource indicates how to scale on a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  The values will be averaged together before being compared to the target.  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.  Only one "target" type should be set."""

    props: List[str] = ["name", "target"]
    required_props: List[str] = ["name", "target"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def target(self) -> io__k8s__api__autoscaling__v2__MetricTarget:
        return self._target

    def __init__(self, name: str, target: io__k8s__api__autoscaling__v2__MetricTarget):
        super().__init__()
        if name is not None:
            self._name = name
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2__ResourceMetricStatus(K8STemplatable):
    """ResourceMetricStatus indicates the current value of a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source."""

    props: List[str] = ["current", "name"]
    required_props: List[str] = ["name", "current"]

    @property
    def current(self) -> io__k8s__api__autoscaling__v2__MetricValueStatus:
        return self._current

    @property
    def name(self) -> str:
        return self._name

    def __init__(
        self, current: io__k8s__api__autoscaling__v2__MetricValueStatus, name: str
    ):
        super().__init__()
        if current is not None:
            self._current = current
        if name is not None:
            self._name = name


class io__k8s__api__autoscaling__v2beta1__ContainerResourceMetricSource(K8STemplatable):
    """ContainerResourceMetricSource indicates how to scale on a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  The values will be averaged together before being compared to the target.  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.  Only one "target" type should be set."""

    props: List[str] = [
        "container",
        "name",
        "targetAverageUtilization",
        "targetAverageValue",
    ]
    required_props: List[str] = ["name", "container"]

    @property
    def container(self) -> str:
        return self._container

    @property
    def name(self) -> str:
        return self._name

    @property
    def targetAverageUtilization(self) -> Optional[int]:
        return self._targetAverageUtilization

    @property
    def targetAverageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._targetAverageValue

    def __init__(
        self,
        container: str,
        name: str,
        targetAverageUtilization: Optional[int] = None,
        targetAverageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
    ):
        super().__init__()
        if container is not None:
            self._container = container
        if name is not None:
            self._name = name
        if targetAverageUtilization is not None:
            self._targetAverageUtilization = targetAverageUtilization
        if targetAverageValue is not None:
            self._targetAverageValue = targetAverageValue


class io__k8s__api__autoscaling__v2beta1__ContainerResourceMetricStatus(K8STemplatable):
    """ContainerResourceMetricStatus indicates the current value of a resource metric known to Kubernetes, as specified in requests and limits, describing a single container in each pod in the current scale target (e.g. CPU or memory).  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source."""

    props: List[str] = [
        "container",
        "currentAverageUtilization",
        "currentAverageValue",
        "name",
    ]
    required_props: List[str] = ["name", "currentAverageValue", "container"]

    @property
    def container(self) -> str:
        return self._container

    @property
    def currentAverageUtilization(self) -> Optional[int]:
        return self._currentAverageUtilization

    @property
    def currentAverageValue(
        self,
    ) -> io__k8s__apimachinery__pkg__api__resource__Quantity:
        return self._currentAverageValue

    @property
    def name(self) -> str:
        return self._name

    def __init__(
        self,
        container: str,
        currentAverageValue: io__k8s__apimachinery__pkg__api__resource__Quantity,
        name: str,
        currentAverageUtilization: Optional[int] = None,
    ):
        super().__init__()
        if container is not None:
            self._container = container
        if currentAverageValue is not None:
            self._currentAverageValue = currentAverageValue
        if name is not None:
            self._name = name
        if currentAverageUtilization is not None:
            self._currentAverageUtilization = currentAverageUtilization


class io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerCondition(
    K8STemplatable
):
    """HorizontalPodAutoscalerCondition describes the state of a HorizontalPodAutoscaler at a certain point."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__autoscaling__v2beta1__ResourceMetricSource(K8STemplatable):
    """ResourceMetricSource indicates how to scale on a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  The values will be averaged together before being compared to the target.  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.  Only one "target" type should be set."""

    props: List[str] = ["name", "targetAverageUtilization", "targetAverageValue"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def targetAverageUtilization(self) -> Optional[int]:
        return self._targetAverageUtilization

    @property
    def targetAverageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._targetAverageValue

    def __init__(
        self,
        name: str,
        targetAverageUtilization: Optional[int] = None,
        targetAverageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if targetAverageUtilization is not None:
            self._targetAverageUtilization = targetAverageUtilization
        if targetAverageValue is not None:
            self._targetAverageValue = targetAverageValue


class io__k8s__api__autoscaling__v2beta1__ResourceMetricStatus(K8STemplatable):
    """ResourceMetricStatus indicates the current value of a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source."""

    props: List[str] = ["currentAverageUtilization", "currentAverageValue", "name"]
    required_props: List[str] = ["name", "currentAverageValue"]

    @property
    def currentAverageUtilization(self) -> Optional[int]:
        return self._currentAverageUtilization

    @property
    def currentAverageValue(
        self,
    ) -> io__k8s__apimachinery__pkg__api__resource__Quantity:
        return self._currentAverageValue

    @property
    def name(self) -> str:
        return self._name

    def __init__(
        self,
        currentAverageValue: io__k8s__apimachinery__pkg__api__resource__Quantity,
        name: str,
        currentAverageUtilization: Optional[int] = None,
    ):
        super().__init__()
        if currentAverageValue is not None:
            self._currentAverageValue = currentAverageValue
        if name is not None:
            self._name = name
        if currentAverageUtilization is not None:
            self._currentAverageUtilization = currentAverageUtilization


class io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerCondition(
    K8STemplatable
):
    """HorizontalPodAutoscalerCondition describes the state of a HorizontalPodAutoscaler at a certain point."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__autoscaling__v2beta2__MetricTarget(K8STemplatable):
    """MetricTarget defines the target value, average value, or average utilization of a specific metric"""

    props: List[str] = ["averageUtilization", "averageValue", "type", "value"]
    required_props: List[str] = ["type"]

    @property
    def averageUtilization(self) -> Optional[int]:
        return self._averageUtilization

    @property
    def averageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._averageValue

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._value

    def __init__(
        self,
        type: str,
        averageUtilization: Optional[int] = None,
        averageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        value: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if averageUtilization is not None:
            self._averageUtilization = averageUtilization
        if averageValue is not None:
            self._averageValue = averageValue
        if value is not None:
            self._value = value


class io__k8s__api__autoscaling__v2beta2__MetricValueStatus(K8STemplatable):
    """MetricValueStatus holds the current value for a metric"""

    props: List[str] = ["averageUtilization", "averageValue", "value"]
    required_props: List[str] = []

    @property
    def averageUtilization(self) -> Optional[int]:
        return self._averageUtilization

    @property
    def averageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._averageValue

    @property
    def value(self) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._value

    def __init__(
        self,
        averageUtilization: Optional[int] = None,
        averageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        value: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
    ):
        super().__init__()
        if averageUtilization is not None:
            self._averageUtilization = averageUtilization
        if averageValue is not None:
            self._averageValue = averageValue
        if value is not None:
            self._value = value


class io__k8s__api__autoscaling__v2beta2__ResourceMetricSource(K8STemplatable):
    """ResourceMetricSource indicates how to scale on a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  The values will be averaged together before being compared to the target.  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.  Only one "target" type should be set."""

    props: List[str] = ["name", "target"]
    required_props: List[str] = ["name", "target"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def target(self) -> io__k8s__api__autoscaling__v2beta2__MetricTarget:
        return self._target

    def __init__(
        self, name: str, target: io__k8s__api__autoscaling__v2beta2__MetricTarget
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2beta2__ResourceMetricStatus(K8STemplatable):
    """ResourceMetricStatus indicates the current value of a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source."""

    props: List[str] = ["current", "name"]
    required_props: List[str] = ["name", "current"]

    @property
    def current(self) -> io__k8s__api__autoscaling__v2beta2__MetricValueStatus:
        return self._current

    @property
    def name(self) -> str:
        return self._name

    def __init__(
        self, current: io__k8s__api__autoscaling__v2beta2__MetricValueStatus, name: str
    ):
        super().__init__()
        if current is not None:
            self._current = current
        if name is not None:
            self._name = name


class io__k8s__api__batch__v1__CronJobStatus(K8STemplatable):
    """CronJobStatus represents the current state of a cron job."""

    props: List[str] = ["active", "lastScheduleTime", "lastSuccessfulTime"]
    required_props: List[str] = []

    @property
    def active(self) -> Optional[List[io__k8s__api__core__v1__ObjectReference]]:
        return self._active

    @property
    def lastScheduleTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastScheduleTime

    @property
    def lastSuccessfulTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastSuccessfulTime

    def __init__(
        self,
        active: Optional[List[io__k8s__api__core__v1__ObjectReference]] = None,
        lastScheduleTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastSuccessfulTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
    ):
        super().__init__()
        if active is not None:
            self._active = active
        if lastScheduleTime is not None:
            self._lastScheduleTime = lastScheduleTime
        if lastSuccessfulTime is not None:
            self._lastSuccessfulTime = lastSuccessfulTime


class io__k8s__api__batch__v1__JobCondition(K8STemplatable):
    """JobCondition describes current state of a job."""

    props: List[str] = [
        "lastProbeTime",
        "lastTransitionTime",
        "message",
        "reason",
        "status",
        "type",
    ]
    required_props: List[str] = ["type", "status"]

    @property
    def lastProbeTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastProbeTime

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastProbeTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastProbeTime is not None:
            self._lastProbeTime = lastProbeTime
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__batch__v1__JobStatus(K8STemplatable):
    """JobStatus represents the current state of a Job."""

    props: List[str] = [
        "active",
        "completedIndexes",
        "completionTime",
        "conditions",
        "failed",
        "ready",
        "startTime",
        "succeeded",
        "uncountedTerminatedPods",
    ]
    required_props: List[str] = []

    @property
    def active(self) -> Optional[int]:
        return self._active

    @property
    def completedIndexes(self) -> Optional[str]:
        return self._completedIndexes

    @property
    def completionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._completionTime

    @property
    def conditions(self) -> Optional[List[io__k8s__api__batch__v1__JobCondition]]:
        return self._conditions

    @property
    def failed(self) -> Optional[int]:
        return self._failed

    @property
    def ready(self) -> Optional[int]:
        return self._ready

    @property
    def startTime(self) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._startTime

    @property
    def succeeded(self) -> Optional[int]:
        return self._succeeded

    @property
    def uncountedTerminatedPods(
        self,
    ) -> Optional[io__k8s__api__batch__v1__UncountedTerminatedPods]:
        return self._uncountedTerminatedPods

    def __init__(
        self,
        active: Optional[int] = None,
        completedIndexes: Optional[str] = None,
        completionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        conditions: Optional[List[io__k8s__api__batch__v1__JobCondition]] = None,
        failed: Optional[int] = None,
        ready: Optional[int] = None,
        startTime: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time] = None,
        succeeded: Optional[int] = None,
        uncountedTerminatedPods: Optional[
            io__k8s__api__batch__v1__UncountedTerminatedPods
        ] = None,
    ):
        super().__init__()
        if active is not None:
            self._active = active
        if completedIndexes is not None:
            self._completedIndexes = completedIndexes
        if completionTime is not None:
            self._completionTime = completionTime
        if conditions is not None:
            self._conditions = conditions
        if failed is not None:
            self._failed = failed
        if ready is not None:
            self._ready = ready
        if startTime is not None:
            self._startTime = startTime
        if succeeded is not None:
            self._succeeded = succeeded
        if uncountedTerminatedPods is not None:
            self._uncountedTerminatedPods = uncountedTerminatedPods


class io__k8s__api__batch__v1beta1__CronJobStatus(K8STemplatable):
    """CronJobStatus represents the current state of a cron job."""

    props: List[str] = ["active", "lastScheduleTime", "lastSuccessfulTime"]
    required_props: List[str] = []

    @property
    def active(self) -> Optional[List[io__k8s__api__core__v1__ObjectReference]]:
        return self._active

    @property
    def lastScheduleTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastScheduleTime

    @property
    def lastSuccessfulTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastSuccessfulTime

    def __init__(
        self,
        active: Optional[List[io__k8s__api__core__v1__ObjectReference]] = None,
        lastScheduleTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastSuccessfulTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
    ):
        super().__init__()
        if active is not None:
            self._active = active
        if lastScheduleTime is not None:
            self._lastScheduleTime = lastScheduleTime
        if lastSuccessfulTime is not None:
            self._lastSuccessfulTime = lastSuccessfulTime


class io__k8s__api__certificates__v1__CertificateSigningRequestCondition(
    K8STemplatable
):
    """CertificateSigningRequestCondition describes a condition of a CertificateSigningRequest object"""

    props: List[str] = [
        "lastTransitionTime",
        "lastUpdateTime",
        "message",
        "reason",
        "status",
        "type",
    ]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def lastUpdateTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastUpdateTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> Literal["Approved", "Denied", "Failed"]:
        return self._type

    def __init__(
        self,
        status: str,
        type: Literal["Approved", "Denied", "Failed"],
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastUpdateTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if lastUpdateTime is not None:
            self._lastUpdateTime = lastUpdateTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__certificates__v1__CertificateSigningRequestStatus(K8STemplatable):
    """CertificateSigningRequestStatus contains conditions used to indicate approved/denied/failed status of the request, and the issued certificate."""

    props: List[str] = ["certificate", "conditions"]
    required_props: List[str] = []

    @property
    def certificate(self) -> Optional[str]:
        return self._certificate

    @property
    def conditions(
        self,
    ) -> Optional[
        List[io__k8s__api__certificates__v1__CertificateSigningRequestCondition]
    ]:
        return self._conditions

    def __init__(
        self,
        certificate: Optional[str] = None,
        conditions: Optional[
            List[io__k8s__api__certificates__v1__CertificateSigningRequestCondition]
        ] = None,
    ):
        super().__init__()
        if certificate is not None:
            self._certificate = certificate
        if conditions is not None:
            self._conditions = conditions


class io__k8s__api__coordination__v1__LeaseSpec(K8STemplatable):
    """LeaseSpec is a specification of a Lease."""

    props: List[str] = [
        "acquireTime",
        "holderIdentity",
        "leaseDurationSeconds",
        "leaseTransitions",
        "renewTime",
    ]
    required_props: List[str] = []

    @property
    def acquireTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime]:
        return self._acquireTime

    @property
    def holderIdentity(self) -> Optional[str]:
        return self._holderIdentity

    @property
    def leaseDurationSeconds(self) -> Optional[int]:
        return self._leaseDurationSeconds

    @property
    def leaseTransitions(self) -> Optional[int]:
        return self._leaseTransitions

    @property
    def renewTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime]:
        return self._renewTime

    def __init__(
        self,
        acquireTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime
        ] = None,
        holderIdentity: Optional[str] = None,
        leaseDurationSeconds: Optional[int] = None,
        leaseTransitions: Optional[int] = None,
        renewTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime
        ] = None,
    ):
        super().__init__()
        if acquireTime is not None:
            self._acquireTime = acquireTime
        if holderIdentity is not None:
            self._holderIdentity = holderIdentity
        if leaseDurationSeconds is not None:
            self._leaseDurationSeconds = leaseDurationSeconds
        if leaseTransitions is not None:
            self._leaseTransitions = leaseTransitions
        if renewTime is not None:
            self._renewTime = renewTime


class io__k8s__api__core__v1__CSIPersistentVolumeSource(K8STemplatable):
    """Represents storage that is managed by an external CSI volume driver (Beta feature)"""

    props: List[str] = [
        "controllerExpandSecretRef",
        "controllerPublishSecretRef",
        "driver",
        "fsType",
        "nodePublishSecretRef",
        "nodeStageSecretRef",
        "readOnly",
        "volumeAttributes",
        "volumeHandle",
    ]
    required_props: List[str] = ["driver", "volumeHandle"]

    @property
    def controllerExpandSecretRef(
        self,
    ) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._controllerExpandSecretRef

    @property
    def controllerPublishSecretRef(
        self,
    ) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._controllerPublishSecretRef

    @property
    def driver(self) -> str:
        return self._driver

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def nodePublishSecretRef(self) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._nodePublishSecretRef

    @property
    def nodeStageSecretRef(self) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._nodeStageSecretRef

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def volumeAttributes(self) -> Optional[Dict[str, str]]:
        return self._volumeAttributes

    @property
    def volumeHandle(self) -> str:
        return self._volumeHandle

    def __init__(
        self,
        driver: str,
        volumeHandle: str,
        controllerExpandSecretRef: Optional[
            io__k8s__api__core__v1__SecretReference
        ] = None,
        controllerPublishSecretRef: Optional[
            io__k8s__api__core__v1__SecretReference
        ] = None,
        fsType: Optional[str] = None,
        nodePublishSecretRef: Optional[io__k8s__api__core__v1__SecretReference] = None,
        nodeStageSecretRef: Optional[io__k8s__api__core__v1__SecretReference] = None,
        readOnly: Optional[bool] = None,
        volumeAttributes: Optional[Dict[str, str]] = None,
    ):
        super().__init__()
        if driver is not None:
            self._driver = driver
        if volumeHandle is not None:
            self._volumeHandle = volumeHandle
        if controllerExpandSecretRef is not None:
            self._controllerExpandSecretRef = controllerExpandSecretRef
        if controllerPublishSecretRef is not None:
            self._controllerPublishSecretRef = controllerPublishSecretRef
        if fsType is not None:
            self._fsType = fsType
        if nodePublishSecretRef is not None:
            self._nodePublishSecretRef = nodePublishSecretRef
        if nodeStageSecretRef is not None:
            self._nodeStageSecretRef = nodeStageSecretRef
        if readOnly is not None:
            self._readOnly = readOnly
        if volumeAttributes is not None:
            self._volumeAttributes = volumeAttributes


class io__k8s__api__core__v1__CSIVolumeSource(K8STemplatable):
    """Represents a source location of a volume to mount, managed by an external CSI driver"""

    props: List[str] = [
        "driver",
        "fsType",
        "nodePublishSecretRef",
        "readOnly",
        "volumeAttributes",
    ]
    required_props: List[str] = ["driver"]

    @property
    def driver(self) -> str:
        return self._driver

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def nodePublishSecretRef(
        self,
    ) -> Optional[io__k8s__api__core__v1__LocalObjectReference]:
        return self._nodePublishSecretRef

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def volumeAttributes(self) -> Optional[Dict[str, str]]:
        return self._volumeAttributes

    def __init__(
        self,
        driver: str,
        fsType: Optional[str] = None,
        nodePublishSecretRef: Optional[
            io__k8s__api__core__v1__LocalObjectReference
        ] = None,
        readOnly: Optional[bool] = None,
        volumeAttributes: Optional[Dict[str, str]] = None,
    ):
        super().__init__()
        if driver is not None:
            self._driver = driver
        if fsType is not None:
            self._fsType = fsType
        if nodePublishSecretRef is not None:
            self._nodePublishSecretRef = nodePublishSecretRef
        if readOnly is not None:
            self._readOnly = readOnly
        if volumeAttributes is not None:
            self._volumeAttributes = volumeAttributes


class io__k8s__api__core__v1__CephFSPersistentVolumeSource(K8STemplatable):
    """Represents a Ceph Filesystem mount that lasts the lifetime of a pod Cephfs volumes do not support ownership management or SELinux relabeling."""

    props: List[str] = [
        "monitors",
        "path",
        "readOnly",
        "secretFile",
        "secretRef",
        "user",
    ]
    required_props: List[str] = ["monitors"]

    @property
    def monitors(self) -> List[str]:
        return self._monitors

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretFile(self) -> Optional[str]:
        return self._secretFile

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._secretRef

    @property
    def user(self) -> Optional[str]:
        return self._user

    def __init__(
        self,
        monitors: List[str],
        path: Optional[str] = None,
        readOnly: Optional[bool] = None,
        secretFile: Optional[str] = None,
        secretRef: Optional[io__k8s__api__core__v1__SecretReference] = None,
        user: Optional[str] = None,
    ):
        super().__init__()
        if monitors is not None:
            self._monitors = monitors
        if path is not None:
            self._path = path
        if readOnly is not None:
            self._readOnly = readOnly
        if secretFile is not None:
            self._secretFile = secretFile
        if secretRef is not None:
            self._secretRef = secretRef
        if user is not None:
            self._user = user


class io__k8s__api__core__v1__CephFSVolumeSource(K8STemplatable):
    """Represents a Ceph Filesystem mount that lasts the lifetime of a pod Cephfs volumes do not support ownership management or SELinux relabeling."""

    props: List[str] = [
        "monitors",
        "path",
        "readOnly",
        "secretFile",
        "secretRef",
        "user",
    ]
    required_props: List[str] = ["monitors"]

    @property
    def monitors(self) -> List[str]:
        return self._monitors

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretFile(self) -> Optional[str]:
        return self._secretFile

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__LocalObjectReference]:
        return self._secretRef

    @property
    def user(self) -> Optional[str]:
        return self._user

    def __init__(
        self,
        monitors: List[str],
        path: Optional[str] = None,
        readOnly: Optional[bool] = None,
        secretFile: Optional[str] = None,
        secretRef: Optional[io__k8s__api__core__v1__LocalObjectReference] = None,
        user: Optional[str] = None,
    ):
        super().__init__()
        if monitors is not None:
            self._monitors = monitors
        if path is not None:
            self._path = path
        if readOnly is not None:
            self._readOnly = readOnly
        if secretFile is not None:
            self._secretFile = secretFile
        if secretRef is not None:
            self._secretRef = secretRef
        if user is not None:
            self._user = user


class io__k8s__api__core__v1__CinderPersistentVolumeSource(K8STemplatable):
    """Represents a cinder volume resource in Openstack. A Cinder volume must exist before mounting to a container. The volume must also be in the same region as the kubelet. Cinder volumes support ownership management and SELinux relabeling."""

    props: List[str] = ["fsType", "readOnly", "secretRef", "volumeID"]
    required_props: List[str] = ["volumeID"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._secretRef

    @property
    def volumeID(self) -> str:
        return self._volumeID

    def __init__(
        self,
        volumeID: str,
        fsType: Optional[str] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__SecretReference] = None,
    ):
        super().__init__()
        if volumeID is not None:
            self._volumeID = volumeID
        if fsType is not None:
            self._fsType = fsType
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef


class io__k8s__api__core__v1__CinderVolumeSource(K8STemplatable):
    """Represents a cinder volume resource in Openstack. A Cinder volume must exist before mounting to a container. The volume must also be in the same region as the kubelet. Cinder volumes support ownership management and SELinux relabeling."""

    props: List[str] = ["fsType", "readOnly", "secretRef", "volumeID"]
    required_props: List[str] = ["volumeID"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__LocalObjectReference]:
        return self._secretRef

    @property
    def volumeID(self) -> str:
        return self._volumeID

    def __init__(
        self,
        volumeID: str,
        fsType: Optional[str] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__LocalObjectReference] = None,
    ):
        super().__init__()
        if volumeID is not None:
            self._volumeID = volumeID
        if fsType is not None:
            self._fsType = fsType
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef


class io__k8s__api__core__v1__ConfigMapProjection(K8STemplatable):
    """Adapts a ConfigMap into a projected volume.

    The contents of the target ConfigMap's Data field will be presented in a projected volume as files using the keys in the Data field as the file names, unless the items element is populated with specific mappings of keys to paths. Note that this is identical to a configmap volume source without the default mode."""

    props: List[str] = ["items", "name", "optional"]
    required_props: List[str] = []

    @property
    def items(self) -> Optional[List[io__k8s__api__core__v1__KeyToPath]]:
        return self._items

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def optional(self) -> Optional[bool]:
        return self._optional

    def __init__(
        self,
        items: Optional[List[io__k8s__api__core__v1__KeyToPath]] = None,
        name: Optional[str] = None,
        optional: Optional[bool] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if name is not None:
            self._name = name
        if optional is not None:
            self._optional = optional


class io__k8s__api__core__v1__ConfigMapVolumeSource(K8STemplatable):
    """Adapts a ConfigMap into a volume.

    The contents of the target ConfigMap's Data field will be presented in a volume as files using the keys in the Data field as the file names, unless the items element is populated with specific mappings of keys to paths. ConfigMap volumes support ownership management and SELinux relabeling."""

    props: List[str] = ["defaultMode", "items", "name", "optional"]
    required_props: List[str] = []

    @property
    def defaultMode(self) -> Optional[int]:
        return self._defaultMode

    @property
    def items(self) -> Optional[List[io__k8s__api__core__v1__KeyToPath]]:
        return self._items

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def optional(self) -> Optional[bool]:
        return self._optional

    def __init__(
        self,
        defaultMode: Optional[int] = None,
        items: Optional[List[io__k8s__api__core__v1__KeyToPath]] = None,
        name: Optional[str] = None,
        optional: Optional[bool] = None,
    ):
        super().__init__()
        if defaultMode is not None:
            self._defaultMode = defaultMode
        if items is not None:
            self._items = items
        if name is not None:
            self._name = name
        if optional is not None:
            self._optional = optional


class io__k8s__api__core__v1__ContainerStateRunning(K8STemplatable):
    """ContainerStateRunning is a running state of a container."""

    props: List[str] = ["startedAt"]
    required_props: List[str] = []

    @property
    def startedAt(self) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._startedAt

    def __init__(
        self,
        startedAt: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time] = None,
    ):
        super().__init__()
        if startedAt is not None:
            self._startedAt = startedAt


class io__k8s__api__core__v1__ContainerStateTerminated(K8STemplatable):
    """ContainerStateTerminated is a terminated state of a container."""

    props: List[str] = [
        "containerID",
        "exitCode",
        "finishedAt",
        "message",
        "reason",
        "signal",
        "startedAt",
    ]
    required_props: List[str] = ["exitCode"]

    @property
    def containerID(self) -> Optional[str]:
        return self._containerID

    @property
    def exitCode(self) -> int:
        return self._exitCode

    @property
    def finishedAt(self) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._finishedAt

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def signal(self) -> Optional[int]:
        return self._signal

    @property
    def startedAt(self) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._startedAt

    def __init__(
        self,
        exitCode: int,
        containerID: Optional[str] = None,
        finishedAt: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
        signal: Optional[int] = None,
        startedAt: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time] = None,
    ):
        super().__init__()
        if exitCode is not None:
            self._exitCode = exitCode
        if containerID is not None:
            self._containerID = containerID
        if finishedAt is not None:
            self._finishedAt = finishedAt
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason
        if signal is not None:
            self._signal = signal
        if startedAt is not None:
            self._startedAt = startedAt


class io__k8s__api__core__v1__EmptyDirVolumeSource(K8STemplatable):
    """Represents an empty directory for a pod. Empty directory volumes support ownership management and SELinux relabeling."""

    props: List[str] = ["medium", "sizeLimit"]
    required_props: List[str] = []

    @property
    def medium(self) -> Optional[str]:
        return self._medium

    @property
    def sizeLimit(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._sizeLimit

    def __init__(
        self,
        medium: Optional[str] = None,
        sizeLimit: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
    ):
        super().__init__()
        if medium is not None:
            self._medium = medium
        if sizeLimit is not None:
            self._sizeLimit = sizeLimit


class io__k8s__api__core__v1__EndpointAddress(K8STemplatable):
    """EndpointAddress is a tuple that describes single IP address."""

    props: List[str] = ["hostname", "ip", "nodeName", "targetRef"]
    required_props: List[str] = ["ip"]

    @property
    def hostname(self) -> Optional[str]:
        return self._hostname

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def nodeName(self) -> Optional[str]:
        return self._nodeName

    @property
    def targetRef(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._targetRef

    def __init__(
        self,
        ip: str,
        hostname: Optional[str] = None,
        nodeName: Optional[str] = None,
        targetRef: Optional[io__k8s__api__core__v1__ObjectReference] = None,
    ):
        super().__init__()
        if ip is not None:
            self._ip = ip
        if hostname is not None:
            self._hostname = hostname
        if nodeName is not None:
            self._nodeName = nodeName
        if targetRef is not None:
            self._targetRef = targetRef


class io__k8s__api__core__v1__EndpointSubset(K8STemplatable):
    """EndpointSubset is a group of addresses with a common set of ports. The expanded set of endpoints is the Cartesian product of Addresses x Ports. For example, given:
      {
        Addresses: [{"ip": "10.10.1.1"}, {"ip": "10.10.2.2"}],
        Ports:     [{"name": "a", "port": 8675}, {"name": "b", "port": 309}]
      }
    The resulting set of endpoints can be viewed as:
        a: [ 10.10.1.1:8675, 10.10.2.2:8675 ],
        b: [ 10.10.1.1:309, 10.10.2.2:309 ]"""

    props: List[str] = ["addresses", "notReadyAddresses", "ports"]
    required_props: List[str] = []

    @property
    def addresses(self) -> Optional[List[io__k8s__api__core__v1__EndpointAddress]]:
        return self._addresses

    @property
    def notReadyAddresses(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__EndpointAddress]]:
        return self._notReadyAddresses

    @property
    def ports(self) -> Optional[List[io__k8s__api__core__v1__EndpointPort]]:
        return self._ports

    def __init__(
        self,
        addresses: Optional[List[io__k8s__api__core__v1__EndpointAddress]] = None,
        notReadyAddresses: Optional[
            List[io__k8s__api__core__v1__EndpointAddress]
        ] = None,
        ports: Optional[List[io__k8s__api__core__v1__EndpointPort]] = None,
    ):
        super().__init__()
        if addresses is not None:
            self._addresses = addresses
        if notReadyAddresses is not None:
            self._notReadyAddresses = notReadyAddresses
        if ports is not None:
            self._ports = ports


class io__k8s__api__core__v1__EnvFromSource(K8STemplatable):
    """EnvFromSource represents the source of a set of ConfigMaps"""

    props: List[str] = ["configMapRef", "prefix", "secretRef"]
    required_props: List[str] = []

    @property
    def configMapRef(self) -> Optional[io__k8s__api__core__v1__ConfigMapEnvSource]:
        return self._configMapRef

    @property
    def prefix(self) -> Optional[str]:
        return self._prefix

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__SecretEnvSource]:
        return self._secretRef

    def __init__(
        self,
        configMapRef: Optional[io__k8s__api__core__v1__ConfigMapEnvSource] = None,
        prefix: Optional[str] = None,
        secretRef: Optional[io__k8s__api__core__v1__SecretEnvSource] = None,
    ):
        super().__init__()
        if configMapRef is not None:
            self._configMapRef = configMapRef
        if prefix is not None:
            self._prefix = prefix
        if secretRef is not None:
            self._secretRef = secretRef


class io__k8s__api__core__v1__EventSeries(K8STemplatable):
    """EventSeries contain information on series of events, i.e. thing that was/is happening continuously for some time."""

    props: List[str] = ["count", "lastObservedTime"]
    required_props: List[str] = []

    @property
    def count(self) -> Optional[int]:
        return self._count

    @property
    def lastObservedTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime]:
        return self._lastObservedTime

    def __init__(
        self,
        count: Optional[int] = None,
        lastObservedTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime
        ] = None,
    ):
        super().__init__()
        if count is not None:
            self._count = count
        if lastObservedTime is not None:
            self._lastObservedTime = lastObservedTime


class io__k8s__api__core__v1__FlexPersistentVolumeSource(K8STemplatable):
    """FlexPersistentVolumeSource represents a generic persistent volume resource that is provisioned/attached using an exec based plugin."""

    props: List[str] = ["driver", "fsType", "options", "readOnly", "secretRef"]
    required_props: List[str] = ["driver"]

    @property
    def driver(self) -> str:
        return self._driver

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def options(self) -> Optional[Dict[str, str]]:
        return self._options

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._secretRef

    def __init__(
        self,
        driver: str,
        fsType: Optional[str] = None,
        options: Optional[Dict[str, str]] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__SecretReference] = None,
    ):
        super().__init__()
        if driver is not None:
            self._driver = driver
        if fsType is not None:
            self._fsType = fsType
        if options is not None:
            self._options = options
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef


class io__k8s__api__core__v1__FlexVolumeSource(K8STemplatable):
    """FlexVolume represents a generic volume resource that is provisioned/attached using an exec based plugin."""

    props: List[str] = ["driver", "fsType", "options", "readOnly", "secretRef"]
    required_props: List[str] = ["driver"]

    @property
    def driver(self) -> str:
        return self._driver

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def options(self) -> Optional[Dict[str, str]]:
        return self._options

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__LocalObjectReference]:
        return self._secretRef

    def __init__(
        self,
        driver: str,
        fsType: Optional[str] = None,
        options: Optional[Dict[str, str]] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__LocalObjectReference] = None,
    ):
        super().__init__()
        if driver is not None:
            self._driver = driver
        if fsType is not None:
            self._fsType = fsType
        if options is not None:
            self._options = options
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef


class io__k8s__api__core__v1__HTTPGetAction(K8STemplatable):
    """HTTPGetAction describes an action based on HTTP Get requests."""

    props: List[str] = ["host", "httpHeaders", "path", "port", "scheme"]
    required_props: List[str] = ["port"]

    @property
    def host(self) -> Optional[str]:
        return self._host

    @property
    def httpHeaders(self) -> Optional[List[io__k8s__api__core__v1__HTTPHeader]]:
        return self._httpHeaders

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def port(self) -> io__k8s__apimachinery__pkg__util__intstr__IntOrString:
        return self._port

    @property
    def scheme(self) -> Optional[Literal["HTTP", "HTTPS"]]:
        return self._scheme

    def __init__(
        self,
        port: io__k8s__apimachinery__pkg__util__intstr__IntOrString,
        host: Optional[str] = None,
        httpHeaders: Optional[List[io__k8s__api__core__v1__HTTPHeader]] = None,
        path: Optional[str] = None,
        scheme: Optional[Literal["HTTP", "HTTPS"]] = None,
    ):
        super().__init__()
        if port is not None:
            self._port = port
        if host is not None:
            self._host = host
        if httpHeaders is not None:
            self._httpHeaders = httpHeaders
        if path is not None:
            self._path = path
        if scheme is not None:
            self._scheme = scheme


class io__k8s__api__core__v1__ISCSIPersistentVolumeSource(K8STemplatable):
    """ISCSIPersistentVolumeSource represents an ISCSI disk. ISCSI volumes can only be mounted as read/write once. ISCSI volumes support ownership management and SELinux relabeling."""

    props: List[str] = [
        "chapAuthDiscovery",
        "chapAuthSession",
        "fsType",
        "initiatorName",
        "iqn",
        "iscsiInterface",
        "lun",
        "portals",
        "readOnly",
        "secretRef",
        "targetPortal",
    ]
    required_props: List[str] = ["targetPortal", "iqn", "lun"]

    @property
    def chapAuthDiscovery(self) -> Optional[bool]:
        return self._chapAuthDiscovery

    @property
    def chapAuthSession(self) -> Optional[bool]:
        return self._chapAuthSession

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def initiatorName(self) -> Optional[str]:
        return self._initiatorName

    @property
    def iqn(self) -> str:
        return self._iqn

    @property
    def iscsiInterface(self) -> Optional[str]:
        return self._iscsiInterface

    @property
    def lun(self) -> int:
        return self._lun

    @property
    def portals(self) -> Optional[List[str]]:
        return self._portals

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._secretRef

    @property
    def targetPortal(self) -> str:
        return self._targetPortal

    def __init__(
        self,
        iqn: str,
        lun: int,
        targetPortal: str,
        chapAuthDiscovery: Optional[bool] = None,
        chapAuthSession: Optional[bool] = None,
        fsType: Optional[str] = None,
        initiatorName: Optional[str] = None,
        iscsiInterface: Optional[str] = None,
        portals: Optional[List[str]] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__SecretReference] = None,
    ):
        super().__init__()
        if iqn is not None:
            self._iqn = iqn
        if lun is not None:
            self._lun = lun
        if targetPortal is not None:
            self._targetPortal = targetPortal
        if chapAuthDiscovery is not None:
            self._chapAuthDiscovery = chapAuthDiscovery
        if chapAuthSession is not None:
            self._chapAuthSession = chapAuthSession
        if fsType is not None:
            self._fsType = fsType
        if initiatorName is not None:
            self._initiatorName = initiatorName
        if iscsiInterface is not None:
            self._iscsiInterface = iscsiInterface
        if portals is not None:
            self._portals = portals
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef


class io__k8s__api__core__v1__ISCSIVolumeSource(K8STemplatable):
    """Represents an ISCSI disk. ISCSI volumes can only be mounted as read/write once. ISCSI volumes support ownership management and SELinux relabeling."""

    props: List[str] = [
        "chapAuthDiscovery",
        "chapAuthSession",
        "fsType",
        "initiatorName",
        "iqn",
        "iscsiInterface",
        "lun",
        "portals",
        "readOnly",
        "secretRef",
        "targetPortal",
    ]
    required_props: List[str] = ["targetPortal", "iqn", "lun"]

    @property
    def chapAuthDiscovery(self) -> Optional[bool]:
        return self._chapAuthDiscovery

    @property
    def chapAuthSession(self) -> Optional[bool]:
        return self._chapAuthSession

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def initiatorName(self) -> Optional[str]:
        return self._initiatorName

    @property
    def iqn(self) -> str:
        return self._iqn

    @property
    def iscsiInterface(self) -> Optional[str]:
        return self._iscsiInterface

    @property
    def lun(self) -> int:
        return self._lun

    @property
    def portals(self) -> Optional[List[str]]:
        return self._portals

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__LocalObjectReference]:
        return self._secretRef

    @property
    def targetPortal(self) -> str:
        return self._targetPortal

    def __init__(
        self,
        iqn: str,
        lun: int,
        targetPortal: str,
        chapAuthDiscovery: Optional[bool] = None,
        chapAuthSession: Optional[bool] = None,
        fsType: Optional[str] = None,
        initiatorName: Optional[str] = None,
        iscsiInterface: Optional[str] = None,
        portals: Optional[List[str]] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__LocalObjectReference] = None,
    ):
        super().__init__()
        if iqn is not None:
            self._iqn = iqn
        if lun is not None:
            self._lun = lun
        if targetPortal is not None:
            self._targetPortal = targetPortal
        if chapAuthDiscovery is not None:
            self._chapAuthDiscovery = chapAuthDiscovery
        if chapAuthSession is not None:
            self._chapAuthSession = chapAuthSession
        if fsType is not None:
            self._fsType = fsType
        if initiatorName is not None:
            self._initiatorName = initiatorName
        if iscsiInterface is not None:
            self._iscsiInterface = iscsiInterface
        if portals is not None:
            self._portals = portals
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef


class io__k8s__api__core__v1__LimitRangeItem(K8STemplatable):
    """LimitRangeItem defines a min/max usage limit for any resource that matches on kind."""

    props: List[str] = [
        "default",
        "defaultRequest",
        "max",
        "maxLimitRequestRatio",
        "min",
        "type",
    ]
    required_props: List[str] = ["type"]

    @property
    def default(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._default

    @property
    def defaultRequest(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._defaultRequest

    @property
    def max(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._max

    @property
    def maxLimitRequestRatio(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._maxLimitRequestRatio

    @property
    def min(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._min

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        default: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        defaultRequest: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        max: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        maxLimitRequestRatio: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        min: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if default is not None:
            self._default = default
        if defaultRequest is not None:
            self._defaultRequest = defaultRequest
        if max is not None:
            self._max = max
        if maxLimitRequestRatio is not None:
            self._maxLimitRequestRatio = maxLimitRequestRatio
        if min is not None:
            self._min = min


class io__k8s__api__core__v1__LimitRangeSpec(K8STemplatable):
    """LimitRangeSpec defines a min/max usage limit for resources that match on kind."""

    props: List[str] = ["limits"]
    required_props: List[str] = ["limits"]

    @property
    def limits(self) -> List[io__k8s__api__core__v1__LimitRangeItem]:
        return self._limits

    def __init__(self, limits: List[io__k8s__api__core__v1__LimitRangeItem]):
        super().__init__()
        if limits is not None:
            self._limits = limits


class io__k8s__api__core__v1__LoadBalancerIngress(K8STemplatable):
    """LoadBalancerIngress represents the status of a load-balancer ingress point: traffic intended for the service should be sent to an ingress point."""

    props: List[str] = ["hostname", "ip", "ports"]
    required_props: List[str] = []

    @property
    def hostname(self) -> Optional[str]:
        return self._hostname

    @property
    def ip(self) -> Optional[str]:
        return self._ip

    @property
    def ports(self) -> Optional[List[io__k8s__api__core__v1__PortStatus]]:
        return self._ports

    def __init__(
        self,
        hostname: Optional[str] = None,
        ip: Optional[str] = None,
        ports: Optional[List[io__k8s__api__core__v1__PortStatus]] = None,
    ):
        super().__init__()
        if hostname is not None:
            self._hostname = hostname
        if ip is not None:
            self._ip = ip
        if ports is not None:
            self._ports = ports


class io__k8s__api__core__v1__LoadBalancerStatus(K8STemplatable):
    """LoadBalancerStatus represents the status of a load-balancer."""

    props: List[str] = ["ingress"]
    required_props: List[str] = []

    @property
    def ingress(self) -> Optional[List[io__k8s__api__core__v1__LoadBalancerIngress]]:
        return self._ingress

    def __init__(
        self,
        ingress: Optional[List[io__k8s__api__core__v1__LoadBalancerIngress]] = None,
    ):
        super().__init__()
        if ingress is not None:
            self._ingress = ingress


class io__k8s__api__core__v1__NamespaceCondition(K8STemplatable):
    """NamespaceCondition contains details about state of namespace."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__core__v1__NamespaceStatus(K8STemplatable):
    """NamespaceStatus is information about the current status of a Namespace."""

    props: List[str] = ["conditions", "phase"]
    required_props: List[str] = []

    @property
    def conditions(self) -> Optional[List[io__k8s__api__core__v1__NamespaceCondition]]:
        return self._conditions

    @property
    def phase(self) -> Optional[Literal["Active", "Terminating"]]:
        return self._phase

    def __init__(
        self,
        conditions: Optional[List[io__k8s__api__core__v1__NamespaceCondition]] = None,
        phase: Optional[Literal["Active", "Terminating"]] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions
        if phase is not None:
            self._phase = phase


class io__k8s__api__core__v1__NodeCondition(K8STemplatable):
    """NodeCondition contains condition information for a node."""

    props: List[str] = [
        "lastHeartbeatTime",
        "lastTransitionTime",
        "message",
        "reason",
        "status",
        "type",
    ]
    required_props: List[str] = ["type", "status"]

    @property
    def lastHeartbeatTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastHeartbeatTime

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastHeartbeatTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastHeartbeatTime is not None:
            self._lastHeartbeatTime = lastHeartbeatTime
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__core__v1__NodeSelector(K8STemplatable):
    """A node selector represents the union of the results of one or more label queries over a set of nodes; that is, it represents the OR of the selectors represented by the node selector terms."""

    props: List[str] = ["nodeSelectorTerms"]
    required_props: List[str] = ["nodeSelectorTerms"]

    @property
    def nodeSelectorTerms(self) -> List[io__k8s__api__core__v1__NodeSelectorTerm]:
        return self._nodeSelectorTerms

    def __init__(
        self, nodeSelectorTerms: List[io__k8s__api__core__v1__NodeSelectorTerm]
    ):
        super().__init__()
        if nodeSelectorTerms is not None:
            self._nodeSelectorTerms = nodeSelectorTerms


class io__k8s__api__core__v1__NodeStatus(K8STemplatable):
    """NodeStatus is information about the current status of a node."""

    props: List[str] = [
        "addresses",
        "allocatable",
        "capacity",
        "conditions",
        "config",
        "daemonEndpoints",
        "images",
        "nodeInfo",
        "phase",
        "volumesAttached",
        "volumesInUse",
    ]
    required_props: List[str] = []

    @property
    def addresses(self) -> Optional[List[io__k8s__api__core__v1__NodeAddress]]:
        return self._addresses

    @property
    def allocatable(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._allocatable

    @property
    def capacity(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._capacity

    @property
    def conditions(self) -> Optional[List[io__k8s__api__core__v1__NodeCondition]]:
        return self._conditions

    @property
    def config(self) -> Optional[io__k8s__api__core__v1__NodeConfigStatus]:
        return self._config

    @property
    def daemonEndpoints(self) -> Optional[io__k8s__api__core__v1__NodeDaemonEndpoints]:
        return self._daemonEndpoints

    @property
    def images(self) -> Optional[List[io__k8s__api__core__v1__ContainerImage]]:
        return self._images

    @property
    def nodeInfo(self) -> Optional[io__k8s__api__core__v1__NodeSystemInfo]:
        return self._nodeInfo

    @property
    def phase(self) -> Optional[Literal["Pending", "Running", "Terminated"]]:
        return self._phase

    @property
    def volumesAttached(self) -> Optional[List[io__k8s__api__core__v1__AttachedVolume]]:
        return self._volumesAttached

    @property
    def volumesInUse(self) -> Optional[List[str]]:
        return self._volumesInUse

    def __init__(
        self,
        addresses: Optional[List[io__k8s__api__core__v1__NodeAddress]] = None,
        allocatable: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        capacity: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        conditions: Optional[List[io__k8s__api__core__v1__NodeCondition]] = None,
        config: Optional[io__k8s__api__core__v1__NodeConfigStatus] = None,
        daemonEndpoints: Optional[io__k8s__api__core__v1__NodeDaemonEndpoints] = None,
        images: Optional[List[io__k8s__api__core__v1__ContainerImage]] = None,
        nodeInfo: Optional[io__k8s__api__core__v1__NodeSystemInfo] = None,
        phase: Optional[Literal["Pending", "Running", "Terminated"]] = None,
        volumesAttached: Optional[List[io__k8s__api__core__v1__AttachedVolume]] = None,
        volumesInUse: Optional[List[str]] = None,
    ):
        super().__init__()
        if addresses is not None:
            self._addresses = addresses
        if allocatable is not None:
            self._allocatable = allocatable
        if capacity is not None:
            self._capacity = capacity
        if conditions is not None:
            self._conditions = conditions
        if config is not None:
            self._config = config
        if daemonEndpoints is not None:
            self._daemonEndpoints = daemonEndpoints
        if images is not None:
            self._images = images
        if nodeInfo is not None:
            self._nodeInfo = nodeInfo
        if phase is not None:
            self._phase = phase
        if volumesAttached is not None:
            self._volumesAttached = volumesAttached
        if volumesInUse is not None:
            self._volumesInUse = volumesInUse


class io__k8s__api__core__v1__PersistentVolumeClaimCondition(K8STemplatable):
    """PersistentVolumeClaimCondition contails details about state of pvc"""

    props: List[str] = [
        "lastProbeTime",
        "lastTransitionTime",
        "message",
        "reason",
        "status",
        "type",
    ]
    required_props: List[str] = ["type", "status"]

    @property
    def lastProbeTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastProbeTime

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastProbeTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastProbeTime is not None:
            self._lastProbeTime = lastProbeTime
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__core__v1__PersistentVolumeClaimStatus(K8STemplatable):
    """PersistentVolumeClaimStatus is the current status of a persistent volume claim."""

    props: List[str] = [
        "accessModes",
        "allocatedResources",
        "capacity",
        "conditions",
        "phase",
        "resizeStatus",
    ]
    required_props: List[str] = []

    @property
    def accessModes(self) -> Optional[List[str]]:
        return self._accessModes

    @property
    def allocatedResources(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._allocatedResources

    @property
    def capacity(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._capacity

    @property
    def conditions(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__PersistentVolumeClaimCondition]]:
        return self._conditions

    @property
    def phase(self) -> Optional[Literal["Bound", "Lost", "Pending"]]:
        return self._phase

    @property
    def resizeStatus(self) -> Optional[str]:
        return self._resizeStatus

    def __init__(
        self,
        accessModes: Optional[List[str]] = None,
        allocatedResources: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        capacity: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        conditions: Optional[
            List[io__k8s__api__core__v1__PersistentVolumeClaimCondition]
        ] = None,
        phase: Optional[Literal["Bound", "Lost", "Pending"]] = None,
        resizeStatus: Optional[str] = None,
    ):
        super().__init__()
        if accessModes is not None:
            self._accessModes = accessModes
        if allocatedResources is not None:
            self._allocatedResources = allocatedResources
        if capacity is not None:
            self._capacity = capacity
        if conditions is not None:
            self._conditions = conditions
        if phase is not None:
            self._phase = phase
        if resizeStatus is not None:
            self._resizeStatus = resizeStatus


class io__k8s__api__core__v1__PodCondition(K8STemplatable):
    """PodCondition contains details for the current condition of this pod."""

    props: List[str] = [
        "lastProbeTime",
        "lastTransitionTime",
        "message",
        "reason",
        "status",
        "type",
    ]
    required_props: List[str] = ["type", "status"]

    @property
    def lastProbeTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastProbeTime

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastProbeTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastProbeTime is not None:
            self._lastProbeTime = lastProbeTime
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__core__v1__PodDNSConfig(K8STemplatable):
    """PodDNSConfig defines the DNS parameters of a pod in addition to those generated from DNSPolicy."""

    props: List[str] = ["nameservers", "options", "searches"]
    required_props: List[str] = []

    @property
    def nameservers(self) -> Optional[List[str]]:
        return self._nameservers

    @property
    def options(self) -> Optional[List[io__k8s__api__core__v1__PodDNSConfigOption]]:
        return self._options

    @property
    def searches(self) -> Optional[List[str]]:
        return self._searches

    def __init__(
        self,
        nameservers: Optional[List[str]] = None,
        options: Optional[List[io__k8s__api__core__v1__PodDNSConfigOption]] = None,
        searches: Optional[List[str]] = None,
    ):
        super().__init__()
        if nameservers is not None:
            self._nameservers = nameservers
        if options is not None:
            self._options = options
        if searches is not None:
            self._searches = searches


class io__k8s__api__core__v1__PodSecurityContext(K8STemplatable):
    """PodSecurityContext holds pod-level security attributes and common container settings. Some fields are also present in container.securityContext.  Field values of container.securityContext take precedence over field values of PodSecurityContext."""

    props: List[str] = [
        "fsGroup",
        "fsGroupChangePolicy",
        "runAsGroup",
        "runAsNonRoot",
        "runAsUser",
        "seLinuxOptions",
        "seccompProfile",
        "supplementalGroups",
        "sysctls",
        "windowsOptions",
    ]
    required_props: List[str] = []

    @property
    def fsGroup(self) -> Optional[int]:
        return self._fsGroup

    @property
    def fsGroupChangePolicy(self) -> Optional[str]:
        return self._fsGroupChangePolicy

    @property
    def runAsGroup(self) -> Optional[int]:
        return self._runAsGroup

    @property
    def runAsNonRoot(self) -> Optional[bool]:
        return self._runAsNonRoot

    @property
    def runAsUser(self) -> Optional[int]:
        return self._runAsUser

    @property
    def seLinuxOptions(self) -> Optional[io__k8s__api__core__v1__SELinuxOptions]:
        return self._seLinuxOptions

    @property
    def seccompProfile(self) -> Optional[io__k8s__api__core__v1__SeccompProfile]:
        return self._seccompProfile

    @property
    def supplementalGroups(self) -> Optional[List[int]]:
        return self._supplementalGroups

    @property
    def sysctls(self) -> Optional[List[io__k8s__api__core__v1__Sysctl]]:
        return self._sysctls

    @property
    def windowsOptions(
        self,
    ) -> Optional[io__k8s__api__core__v1__WindowsSecurityContextOptions]:
        return self._windowsOptions

    def __init__(
        self,
        fsGroup: Optional[int] = None,
        fsGroupChangePolicy: Optional[str] = None,
        runAsGroup: Optional[int] = None,
        runAsNonRoot: Optional[bool] = None,
        runAsUser: Optional[int] = None,
        seLinuxOptions: Optional[io__k8s__api__core__v1__SELinuxOptions] = None,
        seccompProfile: Optional[io__k8s__api__core__v1__SeccompProfile] = None,
        supplementalGroups: Optional[List[int]] = None,
        sysctls: Optional[List[io__k8s__api__core__v1__Sysctl]] = None,
        windowsOptions: Optional[
            io__k8s__api__core__v1__WindowsSecurityContextOptions
        ] = None,
    ):
        super().__init__()
        if fsGroup is not None:
            self._fsGroup = fsGroup
        if fsGroupChangePolicy is not None:
            self._fsGroupChangePolicy = fsGroupChangePolicy
        if runAsGroup is not None:
            self._runAsGroup = runAsGroup
        if runAsNonRoot is not None:
            self._runAsNonRoot = runAsNonRoot
        if runAsUser is not None:
            self._runAsUser = runAsUser
        if seLinuxOptions is not None:
            self._seLinuxOptions = seLinuxOptions
        if seccompProfile is not None:
            self._seccompProfile = seccompProfile
        if supplementalGroups is not None:
            self._supplementalGroups = supplementalGroups
        if sysctls is not None:
            self._sysctls = sysctls
        if windowsOptions is not None:
            self._windowsOptions = windowsOptions


class io__k8s__api__core__v1__RBDPersistentVolumeSource(K8STemplatable):
    """Represents a Rados Block Device mount that lasts the lifetime of a pod. RBD volumes support ownership management and SELinux relabeling."""

    props: List[str] = [
        "fsType",
        "image",
        "keyring",
        "monitors",
        "pool",
        "readOnly",
        "secretRef",
        "user",
    ]
    required_props: List[str] = ["monitors", "image"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def image(self) -> str:
        return self._image

    @property
    def keyring(self) -> Optional[str]:
        return self._keyring

    @property
    def monitors(self) -> List[str]:
        return self._monitors

    @property
    def pool(self) -> Optional[str]:
        return self._pool

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> Optional[io__k8s__api__core__v1__SecretReference]:
        return self._secretRef

    @property
    def user(self) -> Optional[str]:
        return self._user

    def __init__(
        self,
        image: str,
        monitors: List[str],
        fsType: Optional[str] = None,
        keyring: Optional[str] = None,
        pool: Optional[str] = None,
        readOnly: Optional[bool] = None,
        secretRef: Optional[io__k8s__api__core__v1__SecretReference] = None,
        user: Optional[str] = None,
    ):
        super().__init__()
        if image is not None:
            self._image = image
        if monitors is not None:
            self._monitors = monitors
        if fsType is not None:
            self._fsType = fsType
        if keyring is not None:
            self._keyring = keyring
        if pool is not None:
            self._pool = pool
        if readOnly is not None:
            self._readOnly = readOnly
        if secretRef is not None:
            self._secretRef = secretRef
        if user is not None:
            self._user = user


class io__k8s__api__core__v1__ReplicationControllerCondition(K8STemplatable):
    """ReplicationControllerCondition describes the state of a replication controller at a certain point."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__api__core__v1__ReplicationControllerStatus(K8STemplatable):
    """ReplicationControllerStatus represents the current status of a replication controller."""

    props: List[str] = [
        "availableReplicas",
        "conditions",
        "fullyLabeledReplicas",
        "observedGeneration",
        "readyReplicas",
        "replicas",
    ]
    required_props: List[str] = ["replicas"]

    @property
    def availableReplicas(self) -> Optional[int]:
        return self._availableReplicas

    @property
    def conditions(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__ReplicationControllerCondition]]:
        return self._conditions

    @property
    def fullyLabeledReplicas(self) -> Optional[int]:
        return self._fullyLabeledReplicas

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    @property
    def readyReplicas(self) -> Optional[int]:
        return self._readyReplicas

    @property
    def replicas(self) -> int:
        return self._replicas

    def __init__(
        self,
        replicas: int,
        availableReplicas: Optional[int] = None,
        conditions: Optional[
            List[io__k8s__api__core__v1__ReplicationControllerCondition]
        ] = None,
        fullyLabeledReplicas: Optional[int] = None,
        observedGeneration: Optional[int] = None,
        readyReplicas: Optional[int] = None,
    ):
        super().__init__()
        if replicas is not None:
            self._replicas = replicas
        if availableReplicas is not None:
            self._availableReplicas = availableReplicas
        if conditions is not None:
            self._conditions = conditions
        if fullyLabeledReplicas is not None:
            self._fullyLabeledReplicas = fullyLabeledReplicas
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration
        if readyReplicas is not None:
            self._readyReplicas = readyReplicas


class io__k8s__api__core__v1__ResourceFieldSelector(K8STemplatable):
    """ResourceFieldSelector represents container resources (cpu, memory) and their output format"""

    props: List[str] = ["containerName", "divisor", "resource"]
    required_props: List[str] = ["resource"]

    @property
    def containerName(self) -> Optional[str]:
        return self._containerName

    @property
    def divisor(self) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._divisor

    @property
    def resource(self) -> str:
        return self._resource

    def __init__(
        self,
        resource: str,
        containerName: Optional[str] = None,
        divisor: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
    ):
        super().__init__()
        if resource is not None:
            self._resource = resource
        if containerName is not None:
            self._containerName = containerName
        if divisor is not None:
            self._divisor = divisor


class io__k8s__api__core__v1__ResourceQuotaStatus(K8STemplatable):
    """ResourceQuotaStatus defines the enforced hard limits and observed use."""

    props: List[str] = ["hard", "used"]
    required_props: List[str] = []

    @property
    def hard(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._hard

    @property
    def used(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._used

    def __init__(
        self,
        hard: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        used: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
    ):
        super().__init__()
        if hard is not None:
            self._hard = hard
        if used is not None:
            self._used = used


class io__k8s__api__core__v1__ResourceRequirements(K8STemplatable):
    """ResourceRequirements describes the compute resource requirements."""

    props: List[str] = ["limits", "requests"]
    required_props: List[str] = []

    @property
    def limits(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._limits

    @property
    def requests(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._requests

    def __init__(
        self,
        limits: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        requests: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
    ):
        super().__init__()
        if limits is not None:
            self._limits = limits
        if requests is not None:
            self._requests = requests


class io__k8s__api__core__v1__ScaleIOPersistentVolumeSource(K8STemplatable):
    """ScaleIOPersistentVolumeSource represents a persistent ScaleIO volume"""

    props: List[str] = [
        "fsType",
        "gateway",
        "protectionDomain",
        "readOnly",
        "secretRef",
        "sslEnabled",
        "storageMode",
        "storagePool",
        "system",
        "volumeName",
    ]
    required_props: List[str] = ["gateway", "system", "secretRef"]

    @property
    def fsType(self) -> Optional[str]:
        return self._fsType

    @property
    def gateway(self) -> str:
        return self._gateway

    @property
    def protectionDomain(self) -> Optional[str]:
        return self._protectionDomain

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @property
    def secretRef(self) -> io__k8s__api__core__v1__SecretReference:
        return self._secretRef

    @property
    def sslEnabled(self) -> Optional[bool]:
        return self._sslEnabled

    @property
    def storageMode(self) -> Optional[str]:
        return self._storageMode

    @property
    def storagePool(self) -> Optional[str]:
        return self._storagePool

    @property
    def system(self) -> str:
        return self._system

    @property
    def volumeName(self) -> Optional[str]:
        return self._volumeName

    def __init__(
        self,
        gateway: str,
        secretRef: io__k8s__api__core__v1__SecretReference,
        system: str,
        fsType: Optional[str] = None,
        protectionDomain: Optional[str] = None,
        readOnly: Optional[bool] = None,
        sslEnabled: Optional[bool] = None,
        storageMode: Optional[str] = None,
        storagePool: Optional[str] = None,
        volumeName: Optional[str] = None,
    ):
        super().__init__()
        if gateway is not None:
            self._gateway = gateway
        if secretRef is not None:
            self._secretRef = secretRef
        if system is not None:
            self._system = system
        if fsType is not None:
            self._fsType = fsType
        if protectionDomain is not None:
            self._protectionDomain = protectionDomain
        if readOnly is not None:
            self._readOnly = readOnly
        if sslEnabled is not None:
            self._sslEnabled = sslEnabled
        if storageMode is not None:
            self._storageMode = storageMode
        if storagePool is not None:
            self._storagePool = storagePool
        if volumeName is not None:
            self._volumeName = volumeName


class io__k8s__api__core__v1__ScopeSelector(K8STemplatable):
    """A scope selector represents the AND of the selectors represented by the scoped-resource selector requirements."""

    props: List[str] = ["matchExpressions"]
    required_props: List[str] = []

    @property
    def matchExpressions(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__ScopedResourceSelectorRequirement]]:
        return self._matchExpressions

    def __init__(
        self,
        matchExpressions: Optional[
            List[io__k8s__api__core__v1__ScopedResourceSelectorRequirement]
        ] = None,
    ):
        super().__init__()
        if matchExpressions is not None:
            self._matchExpressions = matchExpressions


class io__k8s__api__core__v1__SecurityContext(K8STemplatable):
    """SecurityContext holds security configuration that will be applied to a container. Some fields are present in both SecurityContext and PodSecurityContext.  When both are set, the values in SecurityContext take precedence."""

    props: List[str] = [
        "allowPrivilegeEscalation",
        "capabilities",
        "privileged",
        "procMount",
        "readOnlyRootFilesystem",
        "runAsGroup",
        "runAsNonRoot",
        "runAsUser",
        "seLinuxOptions",
        "seccompProfile",
        "windowsOptions",
    ]
    required_props: List[str] = []

    @property
    def allowPrivilegeEscalation(self) -> Optional[bool]:
        return self._allowPrivilegeEscalation

    @property
    def capabilities(self) -> Optional[io__k8s__api__core__v1__Capabilities]:
        return self._capabilities

    @property
    def privileged(self) -> Optional[bool]:
        return self._privileged

    @property
    def procMount(self) -> Optional[str]:
        return self._procMount

    @property
    def readOnlyRootFilesystem(self) -> Optional[bool]:
        return self._readOnlyRootFilesystem

    @property
    def runAsGroup(self) -> Optional[int]:
        return self._runAsGroup

    @property
    def runAsNonRoot(self) -> Optional[bool]:
        return self._runAsNonRoot

    @property
    def runAsUser(self) -> Optional[int]:
        return self._runAsUser

    @property
    def seLinuxOptions(self) -> Optional[io__k8s__api__core__v1__SELinuxOptions]:
        return self._seLinuxOptions

    @property
    def seccompProfile(self) -> Optional[io__k8s__api__core__v1__SeccompProfile]:
        return self._seccompProfile

    @property
    def windowsOptions(
        self,
    ) -> Optional[io__k8s__api__core__v1__WindowsSecurityContextOptions]:
        return self._windowsOptions

    def __init__(
        self,
        allowPrivilegeEscalation: Optional[bool] = None,
        capabilities: Optional[io__k8s__api__core__v1__Capabilities] = None,
        privileged: Optional[bool] = None,
        procMount: Optional[str] = None,
        readOnlyRootFilesystem: Optional[bool] = None,
        runAsGroup: Optional[int] = None,
        runAsNonRoot: Optional[bool] = None,
        runAsUser: Optional[int] = None,
        seLinuxOptions: Optional[io__k8s__api__core__v1__SELinuxOptions] = None,
        seccompProfile: Optional[io__k8s__api__core__v1__SeccompProfile] = None,
        windowsOptions: Optional[
            io__k8s__api__core__v1__WindowsSecurityContextOptions
        ] = None,
    ):
        super().__init__()
        if allowPrivilegeEscalation is not None:
            self._allowPrivilegeEscalation = allowPrivilegeEscalation
        if capabilities is not None:
            self._capabilities = capabilities
        if privileged is not None:
            self._privileged = privileged
        if procMount is not None:
            self._procMount = procMount
        if readOnlyRootFilesystem is not None:
            self._readOnlyRootFilesystem = readOnlyRootFilesystem
        if runAsGroup is not None:
            self._runAsGroup = runAsGroup
        if runAsNonRoot is not None:
            self._runAsNonRoot = runAsNonRoot
        if runAsUser is not None:
            self._runAsUser = runAsUser
        if seLinuxOptions is not None:
            self._seLinuxOptions = seLinuxOptions
        if seccompProfile is not None:
            self._seccompProfile = seccompProfile
        if windowsOptions is not None:
            self._windowsOptions = windowsOptions


class io__k8s__api__core__v1__ServicePort(K8STemplatable):
    """ServicePort contains information on service's port."""

    props: List[str] = [
        "appProtocol",
        "name",
        "nodePort",
        "port",
        "protocol",
        "targetPort",
    ]
    required_props: List[str] = ["port"]

    @property
    def appProtocol(self) -> Optional[str]:
        return self._appProtocol

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def nodePort(self) -> Optional[int]:
        return self._nodePort

    @property
    def port(self) -> int:
        return self._port

    @property
    def protocol(self) -> Optional[Literal["SCTP", "TCP", "UDP"]]:
        return self._protocol

    @property
    def targetPort(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._targetPort

    def __init__(
        self,
        port: int,
        appProtocol: Optional[str] = None,
        name: Optional[str] = None,
        nodePort: Optional[int] = None,
        protocol: Optional[Literal["SCTP", "TCP", "UDP"]] = None,
        targetPort: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
    ):
        super().__init__()
        if port is not None:
            self._port = port
        if appProtocol is not None:
            self._appProtocol = appProtocol
        if name is not None:
            self._name = name
        if nodePort is not None:
            self._nodePort = nodePort
        if protocol is not None:
            self._protocol = protocol
        if targetPort is not None:
            self._targetPort = targetPort


class io__k8s__api__core__v1__ServiceSpec(K8STemplatable):
    """ServiceSpec describes the attributes that a user creates on a service."""

    props: List[str] = [
        "allocateLoadBalancerNodePorts",
        "clusterIP",
        "clusterIPs",
        "externalIPs",
        "externalName",
        "externalTrafficPolicy",
        "healthCheckNodePort",
        "internalTrafficPolicy",
        "ipFamilies",
        "ipFamilyPolicy",
        "loadBalancerClass",
        "loadBalancerIP",
        "loadBalancerSourceRanges",
        "ports",
        "publishNotReadyAddresses",
        "selector",
        "sessionAffinity",
        "sessionAffinityConfig",
        "type",
    ]
    required_props: List[str] = []

    @property
    def allocateLoadBalancerNodePorts(self) -> Optional[bool]:
        return self._allocateLoadBalancerNodePorts

    @property
    def clusterIP(self) -> Optional[str]:
        return self._clusterIP

    @property
    def clusterIPs(self) -> Optional[List[str]]:
        return self._clusterIPs

    @property
    def externalIPs(self) -> Optional[List[str]]:
        return self._externalIPs

    @property
    def externalName(self) -> Optional[str]:
        return self._externalName

    @property
    def externalTrafficPolicy(self) -> Optional[Literal["Cluster", "Local"]]:
        return self._externalTrafficPolicy

    @property
    def healthCheckNodePort(self) -> Optional[int]:
        return self._healthCheckNodePort

    @property
    def internalTrafficPolicy(self) -> Optional[str]:
        return self._internalTrafficPolicy

    @property
    def ipFamilies(self) -> Optional[List[str]]:
        return self._ipFamilies

    @property
    def ipFamilyPolicy(self) -> Optional[str]:
        return self._ipFamilyPolicy

    @property
    def loadBalancerClass(self) -> Optional[str]:
        return self._loadBalancerClass

    @property
    def loadBalancerIP(self) -> Optional[str]:
        return self._loadBalancerIP

    @property
    def loadBalancerSourceRanges(self) -> Optional[List[str]]:
        return self._loadBalancerSourceRanges

    @property
    def ports(self) -> Optional[List[io__k8s__api__core__v1__ServicePort]]:
        return self._ports

    @property
    def publishNotReadyAddresses(self) -> Optional[bool]:
        return self._publishNotReadyAddresses

    @property
    def selector(self) -> Optional[Dict[str, str]]:
        return self._selector

    @property
    def sessionAffinity(self) -> Optional[Literal["ClientIP", "None"]]:
        return self._sessionAffinity

    @property
    def sessionAffinityConfig(
        self,
    ) -> Optional[io__k8s__api__core__v1__SessionAffinityConfig]:
        return self._sessionAffinityConfig

    @property
    def type(
        self,
    ) -> Optional[Literal["ClusterIP", "ExternalName", "LoadBalancer", "NodePort"]]:
        return self._type

    def __init__(
        self,
        allocateLoadBalancerNodePorts: Optional[bool] = None,
        clusterIP: Optional[str] = None,
        clusterIPs: Optional[List[str]] = None,
        externalIPs: Optional[List[str]] = None,
        externalName: Optional[str] = None,
        externalTrafficPolicy: Optional[Literal["Cluster", "Local"]] = None,
        healthCheckNodePort: Optional[int] = None,
        internalTrafficPolicy: Optional[str] = None,
        ipFamilies: Optional[List[str]] = None,
        ipFamilyPolicy: Optional[str] = None,
        loadBalancerClass: Optional[str] = None,
        loadBalancerIP: Optional[str] = None,
        loadBalancerSourceRanges: Optional[List[str]] = None,
        ports: Optional[List[io__k8s__api__core__v1__ServicePort]] = None,
        publishNotReadyAddresses: Optional[bool] = None,
        selector: Optional[Dict[str, str]] = None,
        sessionAffinity: Optional[Literal["ClientIP", "None"]] = None,
        sessionAffinityConfig: Optional[
            io__k8s__api__core__v1__SessionAffinityConfig
        ] = None,
        type: Optional[
            Literal["ClusterIP", "ExternalName", "LoadBalancer", "NodePort"]
        ] = None,
    ):
        super().__init__()
        if allocateLoadBalancerNodePorts is not None:
            self._allocateLoadBalancerNodePorts = allocateLoadBalancerNodePorts
        if clusterIP is not None:
            self._clusterIP = clusterIP
        if clusterIPs is not None:
            self._clusterIPs = clusterIPs
        if externalIPs is not None:
            self._externalIPs = externalIPs
        if externalName is not None:
            self._externalName = externalName
        if externalTrafficPolicy is not None:
            self._externalTrafficPolicy = externalTrafficPolicy
        if healthCheckNodePort is not None:
            self._healthCheckNodePort = healthCheckNodePort
        if internalTrafficPolicy is not None:
            self._internalTrafficPolicy = internalTrafficPolicy
        if ipFamilies is not None:
            self._ipFamilies = ipFamilies
        if ipFamilyPolicy is not None:
            self._ipFamilyPolicy = ipFamilyPolicy
        if loadBalancerClass is not None:
            self._loadBalancerClass = loadBalancerClass
        if loadBalancerIP is not None:
            self._loadBalancerIP = loadBalancerIP
        if loadBalancerSourceRanges is not None:
            self._loadBalancerSourceRanges = loadBalancerSourceRanges
        if ports is not None:
            self._ports = ports
        if publishNotReadyAddresses is not None:
            self._publishNotReadyAddresses = publishNotReadyAddresses
        if selector is not None:
            self._selector = selector
        if sessionAffinity is not None:
            self._sessionAffinity = sessionAffinity
        if sessionAffinityConfig is not None:
            self._sessionAffinityConfig = sessionAffinityConfig
        if type is not None:
            self._type = type


class io__k8s__api__core__v1__TCPSocketAction(K8STemplatable):
    """TCPSocketAction describes an action based on opening a socket"""

    props: List[str] = ["host", "port"]
    required_props: List[str] = ["port"]

    @property
    def host(self) -> Optional[str]:
        return self._host

    @property
    def port(self) -> io__k8s__apimachinery__pkg__util__intstr__IntOrString:
        return self._port

    def __init__(
        self,
        port: io__k8s__apimachinery__pkg__util__intstr__IntOrString,
        host: Optional[str] = None,
    ):
        super().__init__()
        if port is not None:
            self._port = port
        if host is not None:
            self._host = host


class io__k8s__api__core__v1__Taint(K8STemplatable):
    """The node this Taint is attached to has the "effect" on any pod that does not tolerate the Taint."""

    props: List[str] = ["effect", "key", "timeAdded", "value"]
    required_props: List[str] = ["key", "effect"]

    @property
    def effect(self) -> Literal["NoExecute", "NoSchedule", "PreferNoSchedule"]:
        return self._effect

    @property
    def key(self) -> str:
        return self._key

    @property
    def timeAdded(self) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._timeAdded

    @property
    def value(self) -> Optional[str]:
        return self._value

    def __init__(
        self,
        effect: Literal["NoExecute", "NoSchedule", "PreferNoSchedule"],
        key: str,
        timeAdded: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time] = None,
        value: Optional[str] = None,
    ):
        super().__init__()
        if effect is not None:
            self._effect = effect
        if key is not None:
            self._key = key
        if timeAdded is not None:
            self._timeAdded = timeAdded
        if value is not None:
            self._value = value


class io__k8s__api__core__v1__VolumeNodeAffinity(K8STemplatable):
    """VolumeNodeAffinity defines constraints that limit what nodes this volume can be accessed from."""

    props: List[str] = ["required"]
    required_props: List[str] = []

    @property
    def required(self) -> Optional[io__k8s__api__core__v1__NodeSelector]:
        return self._required

    def __init__(self, required: Optional[io__k8s__api__core__v1__NodeSelector] = None):
        super().__init__()
        if required is not None:
            self._required = required


class io__k8s__api__discovery__v1__EndpointHints(K8STemplatable):
    """EndpointHints provides hints describing how an endpoint should be consumed."""

    props: List[str] = ["forZones"]
    required_props: List[str] = []

    @property
    def forZones(self) -> Optional[List[io__k8s__api__discovery__v1__ForZone]]:
        return self._forZones

    def __init__(
        self, forZones: Optional[List[io__k8s__api__discovery__v1__ForZone]] = None
    ):
        super().__init__()
        if forZones is not None:
            self._forZones = forZones


class io__k8s__api__discovery__v1beta1__EndpointHints(K8STemplatable):
    """EndpointHints provides hints describing how an endpoint should be consumed."""

    props: List[str] = ["forZones"]
    required_props: List[str] = []

    @property
    def forZones(self) -> Optional[List[io__k8s__api__discovery__v1beta1__ForZone]]:
        return self._forZones

    def __init__(
        self, forZones: Optional[List[io__k8s__api__discovery__v1beta1__ForZone]] = None
    ):
        super().__init__()
        if forZones is not None:
            self._forZones = forZones


class io__k8s__api__events__v1__EventSeries(K8STemplatable):
    """EventSeries contain information on series of events, i.e. thing that was/is happening continuously for some time. How often to update the EventSeries is up to the event reporters. The default event reporter in "k8s.io/client-go/tools/events/event_broadcaster.go" shows how this struct is updated on heartbeats and can guide customized reporter implementations."""

    props: List[str] = ["count", "lastObservedTime"]
    required_props: List[str] = ["count", "lastObservedTime"]

    @property
    def count(self) -> int:
        return self._count

    @property
    def lastObservedTime(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime:
        return self._lastObservedTime

    def __init__(
        self,
        count: int,
        lastObservedTime: io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime,
    ):
        super().__init__()
        if count is not None:
            self._count = count
        if lastObservedTime is not None:
            self._lastObservedTime = lastObservedTime


class io__k8s__api__events__v1beta1__EventSeries(K8STemplatable):
    """EventSeries contain information on series of events, i.e. thing that was/is happening continuously for some time."""

    props: List[str] = ["count", "lastObservedTime"]
    required_props: List[str] = ["count", "lastObservedTime"]

    @property
    def count(self) -> int:
        return self._count

    @property
    def lastObservedTime(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime:
        return self._lastObservedTime

    def __init__(
        self,
        count: int,
        lastObservedTime: io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime,
    ):
        super().__init__()
        if count is not None:
            self._count = count
        if lastObservedTime is not None:
            self._lastObservedTime = lastObservedTime


class io__k8s__api__flowcontrol__v1beta1__FlowSchemaCondition(K8STemplatable):
    """FlowSchemaCondition describes conditions for a FlowSchema."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = []

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> Optional[str]:
        return self._status

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(
        self,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
        status: Optional[str] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type


class io__k8s__api__flowcontrol__v1beta1__FlowSchemaStatus(K8STemplatable):
    """FlowSchemaStatus represents the current state of a FlowSchema."""

    props: List[str] = ["conditions"]
    required_props: List[str] = []

    @property
    def conditions(
        self,
    ) -> Optional[List[io__k8s__api__flowcontrol__v1beta1__FlowSchemaCondition]]:
        return self._conditions

    def __init__(
        self,
        conditions: Optional[
            List[io__k8s__api__flowcontrol__v1beta1__FlowSchemaCondition]
        ] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions


class io__k8s__api__flowcontrol__v1beta1__LimitResponse(K8STemplatable):
    """LimitResponse defines how to handle requests that can not be executed right now."""

    props: List[str] = ["queuing", "type"]
    required_props: List[str] = ["type"]

    @property
    def queuing(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta1__QueuingConfiguration]:
        return self._queuing

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        queuing: Optional[
            io__k8s__api__flowcontrol__v1beta1__QueuingConfiguration
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if queuing is not None:
            self._queuing = queuing


class io__k8s__api__flowcontrol__v1beta1__LimitedPriorityLevelConfiguration(
    K8STemplatable
):
    """LimitedPriorityLevelConfiguration specifies how to handle requests that are subject to limits. It addresses two issues:
    * How are requests for this priority level limited?
    * What should be done with requests that exceed the limit?"""

    props: List[str] = ["assuredConcurrencyShares", "limitResponse"]
    required_props: List[str] = []

    @property
    def assuredConcurrencyShares(self) -> Optional[int]:
        return self._assuredConcurrencyShares

    @property
    def limitResponse(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta1__LimitResponse]:
        return self._limitResponse

    def __init__(
        self,
        assuredConcurrencyShares: Optional[int] = None,
        limitResponse: Optional[
            io__k8s__api__flowcontrol__v1beta1__LimitResponse
        ] = None,
    ):
        super().__init__()
        if assuredConcurrencyShares is not None:
            self._assuredConcurrencyShares = assuredConcurrencyShares
        if limitResponse is not None:
            self._limitResponse = limitResponse


class io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationCondition(
    K8STemplatable
):
    """PriorityLevelConfigurationCondition defines the condition of priority level."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = []

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> Optional[str]:
        return self._status

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(
        self,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
        status: Optional[str] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type


class io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationSpec(
    K8STemplatable
):
    """PriorityLevelConfigurationSpec specifies the configuration of a priority level."""

    props: List[str] = ["limited", "type"]
    required_props: List[str] = ["type"]

    @property
    def limited(
        self,
    ) -> Optional[
        io__k8s__api__flowcontrol__v1beta1__LimitedPriorityLevelConfiguration
    ]:
        return self._limited

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        limited: Optional[
            io__k8s__api__flowcontrol__v1beta1__LimitedPriorityLevelConfiguration
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if limited is not None:
            self._limited = limited


class io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationStatus(
    K8STemplatable
):
    """PriorityLevelConfigurationStatus represents the current state of a "request-priority"."""

    props: List[str] = ["conditions"]
    required_props: List[str] = []

    @property
    def conditions(
        self,
    ) -> Optional[
        List[io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationCondition]
    ]:
        return self._conditions

    def __init__(
        self,
        conditions: Optional[
            List[
                io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationCondition
            ]
        ] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions


class io__k8s__api__flowcontrol__v1beta1__Subject(K8STemplatable):
    """Subject matches the originator of a request, as identified by the request authentication system. There are three ways of matching an originator; by user, group, or service account."""

    props: List[str] = ["group", "kind", "serviceAccount", "user"]
    required_props: List[str] = ["kind"]

    @property
    def group(self) -> Optional[io__k8s__api__flowcontrol__v1beta1__GroupSubject]:
        return self._group

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def serviceAccount(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta1__ServiceAccountSubject]:
        return self._serviceAccount

    @property
    def user(self) -> Optional[io__k8s__api__flowcontrol__v1beta1__UserSubject]:
        return self._user

    def __init__(
        self,
        kind: str,
        group: Optional[io__k8s__api__flowcontrol__v1beta1__GroupSubject] = None,
        serviceAccount: Optional[
            io__k8s__api__flowcontrol__v1beta1__ServiceAccountSubject
        ] = None,
        user: Optional[io__k8s__api__flowcontrol__v1beta1__UserSubject] = None,
    ):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if group is not None:
            self._group = group
        if serviceAccount is not None:
            self._serviceAccount = serviceAccount
        if user is not None:
            self._user = user


class io__k8s__api__flowcontrol__v1beta2__FlowSchemaCondition(K8STemplatable):
    """FlowSchemaCondition describes conditions for a FlowSchema."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = []

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> Optional[str]:
        return self._status

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(
        self,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
        status: Optional[str] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type


class io__k8s__api__flowcontrol__v1beta2__FlowSchemaStatus(K8STemplatable):
    """FlowSchemaStatus represents the current state of a FlowSchema."""

    props: List[str] = ["conditions"]
    required_props: List[str] = []

    @property
    def conditions(
        self,
    ) -> Optional[List[io__k8s__api__flowcontrol__v1beta2__FlowSchemaCondition]]:
        return self._conditions

    def __init__(
        self,
        conditions: Optional[
            List[io__k8s__api__flowcontrol__v1beta2__FlowSchemaCondition]
        ] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions


class io__k8s__api__flowcontrol__v1beta2__LimitResponse(K8STemplatable):
    """LimitResponse defines how to handle requests that can not be executed right now."""

    props: List[str] = ["queuing", "type"]
    required_props: List[str] = ["type"]

    @property
    def queuing(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta2__QueuingConfiguration]:
        return self._queuing

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        queuing: Optional[
            io__k8s__api__flowcontrol__v1beta2__QueuingConfiguration
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if queuing is not None:
            self._queuing = queuing


class io__k8s__api__flowcontrol__v1beta2__LimitedPriorityLevelConfiguration(
    K8STemplatable
):
    """LimitedPriorityLevelConfiguration specifies how to handle requests that are subject to limits. It addresses two issues:
    * How are requests for this priority level limited?
    * What should be done with requests that exceed the limit?"""

    props: List[str] = ["assuredConcurrencyShares", "limitResponse"]
    required_props: List[str] = []

    @property
    def assuredConcurrencyShares(self) -> Optional[int]:
        return self._assuredConcurrencyShares

    @property
    def limitResponse(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta2__LimitResponse]:
        return self._limitResponse

    def __init__(
        self,
        assuredConcurrencyShares: Optional[int] = None,
        limitResponse: Optional[
            io__k8s__api__flowcontrol__v1beta2__LimitResponse
        ] = None,
    ):
        super().__init__()
        if assuredConcurrencyShares is not None:
            self._assuredConcurrencyShares = assuredConcurrencyShares
        if limitResponse is not None:
            self._limitResponse = limitResponse


class io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationCondition(
    K8STemplatable
):
    """PriorityLevelConfigurationCondition defines the condition of priority level."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = []

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> Optional[str]:
        return self._status

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(
        self,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
        status: Optional[str] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type


class io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationSpec(
    K8STemplatable
):
    """PriorityLevelConfigurationSpec specifies the configuration of a priority level."""

    props: List[str] = ["limited", "type"]
    required_props: List[str] = ["type"]

    @property
    def limited(
        self,
    ) -> Optional[
        io__k8s__api__flowcontrol__v1beta2__LimitedPriorityLevelConfiguration
    ]:
        return self._limited

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        limited: Optional[
            io__k8s__api__flowcontrol__v1beta2__LimitedPriorityLevelConfiguration
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if limited is not None:
            self._limited = limited


class io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationStatus(
    K8STemplatable
):
    """PriorityLevelConfigurationStatus represents the current state of a "request-priority"."""

    props: List[str] = ["conditions"]
    required_props: List[str] = []

    @property
    def conditions(
        self,
    ) -> Optional[
        List[io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationCondition]
    ]:
        return self._conditions

    def __init__(
        self,
        conditions: Optional[
            List[
                io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationCondition
            ]
        ] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions


class io__k8s__api__flowcontrol__v1beta2__Subject(K8STemplatable):
    """Subject matches the originator of a request, as identified by the request authentication system. There are three ways of matching an originator; by user, group, or service account."""

    props: List[str] = ["group", "kind", "serviceAccount", "user"]
    required_props: List[str] = ["kind"]

    @property
    def group(self) -> Optional[io__k8s__api__flowcontrol__v1beta2__GroupSubject]:
        return self._group

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def serviceAccount(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta2__ServiceAccountSubject]:
        return self._serviceAccount

    @property
    def user(self) -> Optional[io__k8s__api__flowcontrol__v1beta2__UserSubject]:
        return self._user

    def __init__(
        self,
        kind: str,
        group: Optional[io__k8s__api__flowcontrol__v1beta2__GroupSubject] = None,
        serviceAccount: Optional[
            io__k8s__api__flowcontrol__v1beta2__ServiceAccountSubject
        ] = None,
        user: Optional[io__k8s__api__flowcontrol__v1beta2__UserSubject] = None,
    ):
        super().__init__()
        if kind is not None:
            self._kind = kind
        if group is not None:
            self._group = group
        if serviceAccount is not None:
            self._serviceAccount = serviceAccount
        if user is not None:
            self._user = user


class io__k8s__api__networking__v1__IngressServiceBackend(K8STemplatable):
    """IngressServiceBackend references a Kubernetes Service as a Backend."""

    props: List[str] = ["name", "port"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def port(self) -> Optional[io__k8s__api__networking__v1__ServiceBackendPort]:
        return self._port

    def __init__(
        self,
        name: str,
        port: Optional[io__k8s__api__networking__v1__ServiceBackendPort] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if port is not None:
            self._port = port


class io__k8s__api__networking__v1__IngressStatus(K8STemplatable):
    """IngressStatus describe the current state of the Ingress."""

    props: List[str] = ["loadBalancer"]
    required_props: List[str] = []

    @property
    def loadBalancer(self) -> Optional[io__k8s__api__core__v1__LoadBalancerStatus]:
        return self._loadBalancer

    def __init__(
        self, loadBalancer: Optional[io__k8s__api__core__v1__LoadBalancerStatus] = None
    ):
        super().__init__()
        if loadBalancer is not None:
            self._loadBalancer = loadBalancer


class io__k8s__api__networking__v1__NetworkPolicyPort(K8STemplatable):
    """NetworkPolicyPort describes a port to allow traffic on"""

    props: List[str] = ["endPort", "port", "protocol"]
    required_props: List[str] = []

    @property
    def endPort(self) -> Optional[int]:
        return self._endPort

    @property
    def port(self) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._port

    @property
    def protocol(self) -> Optional[str]:
        return self._protocol

    def __init__(
        self,
        endPort: Optional[int] = None,
        port: Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString] = None,
        protocol: Optional[str] = None,
    ):
        super().__init__()
        if endPort is not None:
            self._endPort = endPort
        if port is not None:
            self._port = port
        if protocol is not None:
            self._protocol = protocol


class io__k8s__api__node__v1__Overhead(K8STemplatable):
    """Overhead structure represents the resource overhead associated with running a pod."""

    props: List[str] = ["podFixed"]
    required_props: List[str] = []

    @property
    def podFixed(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._podFixed

    def __init__(
        self,
        podFixed: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
    ):
        super().__init__()
        if podFixed is not None:
            self._podFixed = podFixed


class io__k8s__api__node__v1beta1__Overhead(K8STemplatable):
    """Overhead structure represents the resource overhead associated with running a pod."""

    props: List[str] = ["podFixed"]
    required_props: List[str] = []

    @property
    def podFixed(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._podFixed

    def __init__(
        self,
        podFixed: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
    ):
        super().__init__()
        if podFixed is not None:
            self._podFixed = podFixed


class io__k8s__api__policy__v1beta1__FSGroupStrategyOptions(K8STemplatable):
    """FSGroupStrategyOptions defines the strategy type and options used to create the strategy."""

    props: List[str] = ["ranges", "rule"]
    required_props: List[str] = []

    @property
    def ranges(self) -> Optional[List[io__k8s__api__policy__v1beta1__IDRange]]:
        return self._ranges

    @property
    def rule(self) -> Optional[str]:
        return self._rule

    def __init__(
        self,
        ranges: Optional[List[io__k8s__api__policy__v1beta1__IDRange]] = None,
        rule: Optional[str] = None,
    ):
        super().__init__()
        if ranges is not None:
            self._ranges = ranges
        if rule is not None:
            self._rule = rule


class io__k8s__api__policy__v1beta1__PodSecurityPolicySpec(K8STemplatable):
    """PodSecurityPolicySpec defines the policy enforced."""

    props: List[str] = [
        "allowPrivilegeEscalation",
        "allowedCSIDrivers",
        "allowedCapabilities",
        "allowedFlexVolumes",
        "allowedHostPaths",
        "allowedProcMountTypes",
        "allowedUnsafeSysctls",
        "defaultAddCapabilities",
        "defaultAllowPrivilegeEscalation",
        "forbiddenSysctls",
        "fsGroup",
        "hostIPC",
        "hostNetwork",
        "hostPID",
        "hostPorts",
        "privileged",
        "readOnlyRootFilesystem",
        "requiredDropCapabilities",
        "runAsGroup",
        "runAsUser",
        "runtimeClass",
        "seLinux",
        "supplementalGroups",
        "volumes",
    ]
    required_props: List[str] = [
        "seLinux",
        "runAsUser",
        "supplementalGroups",
        "fsGroup",
    ]

    @property
    def allowPrivilegeEscalation(self) -> Optional[bool]:
        return self._allowPrivilegeEscalation

    @property
    def allowedCSIDrivers(
        self,
    ) -> Optional[List[io__k8s__api__policy__v1beta1__AllowedCSIDriver]]:
        return self._allowedCSIDrivers

    @property
    def allowedCapabilities(self) -> Optional[List[str]]:
        return self._allowedCapabilities

    @property
    def allowedFlexVolumes(
        self,
    ) -> Optional[List[io__k8s__api__policy__v1beta1__AllowedFlexVolume]]:
        return self._allowedFlexVolumes

    @property
    def allowedHostPaths(
        self,
    ) -> Optional[List[io__k8s__api__policy__v1beta1__AllowedHostPath]]:
        return self._allowedHostPaths

    @property
    def allowedProcMountTypes(self) -> Optional[List[str]]:
        return self._allowedProcMountTypes

    @property
    def allowedUnsafeSysctls(self) -> Optional[List[str]]:
        return self._allowedUnsafeSysctls

    @property
    def defaultAddCapabilities(self) -> Optional[List[str]]:
        return self._defaultAddCapabilities

    @property
    def defaultAllowPrivilegeEscalation(self) -> Optional[bool]:
        return self._defaultAllowPrivilegeEscalation

    @property
    def forbiddenSysctls(self) -> Optional[List[str]]:
        return self._forbiddenSysctls

    @property
    def fsGroup(self) -> io__k8s__api__policy__v1beta1__FSGroupStrategyOptions:
        return self._fsGroup

    @property
    def hostIPC(self) -> Optional[bool]:
        return self._hostIPC

    @property
    def hostNetwork(self) -> Optional[bool]:
        return self._hostNetwork

    @property
    def hostPID(self) -> Optional[bool]:
        return self._hostPID

    @property
    def hostPorts(self) -> Optional[List[io__k8s__api__policy__v1beta1__HostPortRange]]:
        return self._hostPorts

    @property
    def privileged(self) -> Optional[bool]:
        return self._privileged

    @property
    def readOnlyRootFilesystem(self) -> Optional[bool]:
        return self._readOnlyRootFilesystem

    @property
    def requiredDropCapabilities(self) -> Optional[List[str]]:
        return self._requiredDropCapabilities

    @property
    def runAsGroup(
        self,
    ) -> Optional[io__k8s__api__policy__v1beta1__RunAsGroupStrategyOptions]:
        return self._runAsGroup

    @property
    def runAsUser(self) -> io__k8s__api__policy__v1beta1__RunAsUserStrategyOptions:
        return self._runAsUser

    @property
    def runtimeClass(
        self,
    ) -> Optional[io__k8s__api__policy__v1beta1__RuntimeClassStrategyOptions]:
        return self._runtimeClass

    @property
    def seLinux(self) -> io__k8s__api__policy__v1beta1__SELinuxStrategyOptions:
        return self._seLinux

    @property
    def supplementalGroups(
        self,
    ) -> io__k8s__api__policy__v1beta1__SupplementalGroupsStrategyOptions:
        return self._supplementalGroups

    @property
    def volumes(self) -> Optional[List[str]]:
        return self._volumes

    def __init__(
        self,
        fsGroup: io__k8s__api__policy__v1beta1__FSGroupStrategyOptions,
        runAsUser: io__k8s__api__policy__v1beta1__RunAsUserStrategyOptions,
        seLinux: io__k8s__api__policy__v1beta1__SELinuxStrategyOptions,
        supplementalGroups: io__k8s__api__policy__v1beta1__SupplementalGroupsStrategyOptions,
        allowPrivilegeEscalation: Optional[bool] = None,
        allowedCSIDrivers: Optional[
            List[io__k8s__api__policy__v1beta1__AllowedCSIDriver]
        ] = None,
        allowedCapabilities: Optional[List[str]] = None,
        allowedFlexVolumes: Optional[
            List[io__k8s__api__policy__v1beta1__AllowedFlexVolume]
        ] = None,
        allowedHostPaths: Optional[
            List[io__k8s__api__policy__v1beta1__AllowedHostPath]
        ] = None,
        allowedProcMountTypes: Optional[List[str]] = None,
        allowedUnsafeSysctls: Optional[List[str]] = None,
        defaultAddCapabilities: Optional[List[str]] = None,
        defaultAllowPrivilegeEscalation: Optional[bool] = None,
        forbiddenSysctls: Optional[List[str]] = None,
        hostIPC: Optional[bool] = None,
        hostNetwork: Optional[bool] = None,
        hostPID: Optional[bool] = None,
        hostPorts: Optional[List[io__k8s__api__policy__v1beta1__HostPortRange]] = None,
        privileged: Optional[bool] = None,
        readOnlyRootFilesystem: Optional[bool] = None,
        requiredDropCapabilities: Optional[List[str]] = None,
        runAsGroup: Optional[
            io__k8s__api__policy__v1beta1__RunAsGroupStrategyOptions
        ] = None,
        runtimeClass: Optional[
            io__k8s__api__policy__v1beta1__RuntimeClassStrategyOptions
        ] = None,
        volumes: Optional[List[str]] = None,
    ):
        super().__init__()
        if fsGroup is not None:
            self._fsGroup = fsGroup
        if runAsUser is not None:
            self._runAsUser = runAsUser
        if seLinux is not None:
            self._seLinux = seLinux
        if supplementalGroups is not None:
            self._supplementalGroups = supplementalGroups
        if allowPrivilegeEscalation is not None:
            self._allowPrivilegeEscalation = allowPrivilegeEscalation
        if allowedCSIDrivers is not None:
            self._allowedCSIDrivers = allowedCSIDrivers
        if allowedCapabilities is not None:
            self._allowedCapabilities = allowedCapabilities
        if allowedFlexVolumes is not None:
            self._allowedFlexVolumes = allowedFlexVolumes
        if allowedHostPaths is not None:
            self._allowedHostPaths = allowedHostPaths
        if allowedProcMountTypes is not None:
            self._allowedProcMountTypes = allowedProcMountTypes
        if allowedUnsafeSysctls is not None:
            self._allowedUnsafeSysctls = allowedUnsafeSysctls
        if defaultAddCapabilities is not None:
            self._defaultAddCapabilities = defaultAddCapabilities
        if defaultAllowPrivilegeEscalation is not None:
            self._defaultAllowPrivilegeEscalation = defaultAllowPrivilegeEscalation
        if forbiddenSysctls is not None:
            self._forbiddenSysctls = forbiddenSysctls
        if hostIPC is not None:
            self._hostIPC = hostIPC
        if hostNetwork is not None:
            self._hostNetwork = hostNetwork
        if hostPID is not None:
            self._hostPID = hostPID
        if hostPorts is not None:
            self._hostPorts = hostPorts
        if privileged is not None:
            self._privileged = privileged
        if readOnlyRootFilesystem is not None:
            self._readOnlyRootFilesystem = readOnlyRootFilesystem
        if requiredDropCapabilities is not None:
            self._requiredDropCapabilities = requiredDropCapabilities
        if runAsGroup is not None:
            self._runAsGroup = runAsGroup
        if runtimeClass is not None:
            self._runtimeClass = runtimeClass
        if volumes is not None:
            self._volumes = volumes


class io__k8s__api__storage__v1__CSIDriverSpec(K8STemplatable):
    """CSIDriverSpec is the specification of a CSIDriver."""

    props: List[str] = [
        "attachRequired",
        "fsGroupPolicy",
        "podInfoOnMount",
        "requiresRepublish",
        "storageCapacity",
        "tokenRequests",
        "volumeLifecycleModes",
    ]
    required_props: List[str] = []

    @property
    def attachRequired(self) -> Optional[bool]:
        return self._attachRequired

    @property
    def fsGroupPolicy(self) -> Optional[str]:
        return self._fsGroupPolicy

    @property
    def podInfoOnMount(self) -> Optional[bool]:
        return self._podInfoOnMount

    @property
    def requiresRepublish(self) -> Optional[bool]:
        return self._requiresRepublish

    @property
    def storageCapacity(self) -> Optional[bool]:
        return self._storageCapacity

    @property
    def tokenRequests(self) -> Optional[List[io__k8s__api__storage__v1__TokenRequest]]:
        return self._tokenRequests

    @property
    def volumeLifecycleModes(self) -> Optional[List[str]]:
        return self._volumeLifecycleModes

    def __init__(
        self,
        attachRequired: Optional[bool] = None,
        fsGroupPolicy: Optional[str] = None,
        podInfoOnMount: Optional[bool] = None,
        requiresRepublish: Optional[bool] = None,
        storageCapacity: Optional[bool] = None,
        tokenRequests: Optional[List[io__k8s__api__storage__v1__TokenRequest]] = None,
        volumeLifecycleModes: Optional[List[str]] = None,
    ):
        super().__init__()
        if attachRequired is not None:
            self._attachRequired = attachRequired
        if fsGroupPolicy is not None:
            self._fsGroupPolicy = fsGroupPolicy
        if podInfoOnMount is not None:
            self._podInfoOnMount = podInfoOnMount
        if requiresRepublish is not None:
            self._requiresRepublish = requiresRepublish
        if storageCapacity is not None:
            self._storageCapacity = storageCapacity
        if tokenRequests is not None:
            self._tokenRequests = tokenRequests
        if volumeLifecycleModes is not None:
            self._volumeLifecycleModes = volumeLifecycleModes


class io__k8s__api__storage__v1__CSINodeDriver(K8STemplatable):
    """CSINodeDriver holds information about the specification of one CSI driver installed on a node"""

    props: List[str] = ["allocatable", "name", "nodeID", "topologyKeys"]
    required_props: List[str] = ["name", "nodeID"]

    @property
    def allocatable(self) -> Optional[io__k8s__api__storage__v1__VolumeNodeResources]:
        return self._allocatable

    @property
    def name(self) -> str:
        return self._name

    @property
    def nodeID(self) -> str:
        return self._nodeID

    @property
    def topologyKeys(self) -> Optional[List[str]]:
        return self._topologyKeys

    def __init__(
        self,
        name: str,
        nodeID: str,
        allocatable: Optional[io__k8s__api__storage__v1__VolumeNodeResources] = None,
        topologyKeys: Optional[List[str]] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if nodeID is not None:
            self._nodeID = nodeID
        if allocatable is not None:
            self._allocatable = allocatable
        if topologyKeys is not None:
            self._topologyKeys = topologyKeys


class io__k8s__api__storage__v1__CSINodeSpec(K8STemplatable):
    """CSINodeSpec holds information about the specification of all CSI drivers installed on a node"""

    props: List[str] = ["drivers"]
    required_props: List[str] = ["drivers"]

    @property
    def drivers(self) -> List[io__k8s__api__storage__v1__CSINodeDriver]:
        return self._drivers

    def __init__(self, drivers: List[io__k8s__api__storage__v1__CSINodeDriver]):
        super().__init__()
        if drivers is not None:
            self._drivers = drivers


class io__k8s__api__storage__v1__VolumeError(K8STemplatable):
    """VolumeError captures an error encountered during a volume operation."""

    props: List[str] = ["message", "time"]
    required_props: List[str] = []

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def time(self) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._time

    def __init__(
        self,
        message: Optional[str] = None,
        time: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time] = None,
    ):
        super().__init__()
        if message is not None:
            self._message = message
        if time is not None:
            self._time = time


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceConversion(
    K8STemplatable
):
    """CustomResourceConversion describes how to convert different versions of a CR."""

    props: List[str] = ["strategy", "webhook"]
    required_props: List[str] = ["strategy"]

    @property
    def strategy(self) -> str:
        return self._strategy

    @property
    def webhook(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__WebhookConversion
    ]:
        return self._webhook

    def __init__(
        self,
        strategy: str,
        webhook: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__WebhookConversion
        ] = None,
    ):
        super().__init__()
        if strategy is not None:
            self._strategy = strategy
        if webhook is not None:
            self._webhook = webhook


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionCondition(
    K8STemplatable
):
    """CustomResourceDefinitionCondition contains details for the current condition of this pod."""

    props: List[str] = ["lastTransitionTime", "message", "reason", "status", "type"]
    required_props: List[str] = ["type", "status"]

    @property
    def lastTransitionTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTransitionTime

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        status: str,
        type: str,
        lastTransitionTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionStatus(
    K8STemplatable
):
    """CustomResourceDefinitionStatus indicates the state of the CustomResourceDefinition"""

    props: List[str] = ["acceptedNames", "conditions", "storedVersions"]
    required_props: List[str] = []

    @property
    def acceptedNames(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionNames
    ]:
        return self._acceptedNames

    @property
    def conditions(
        self,
    ) -> Optional[
        List[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionCondition
        ]
    ]:
        return self._conditions

    @property
    def storedVersions(self) -> Optional[List[str]]:
        return self._storedVersions

    def __init__(
        self,
        acceptedNames: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionNames
        ] = None,
        conditions: Optional[
            List[
                io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionCondition
            ]
        ] = None,
        storedVersions: Optional[List[str]] = None,
    ):
        super().__init__()
        if acceptedNames is not None:
            self._acceptedNames = acceptedNames
        if conditions is not None:
            self._conditions = conditions
        if storedVersions is not None:
            self._storedVersions = storedVersions


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaProps(
    K8STemplatable
):
    """JSONSchemaProps is a JSON-Schema following Specification Draft 4 (http://json-schema.org/)."""

    props: List[str] = [
        "S_ref",
        "S_schema",
        "additionalItems",
        "additionalProperties",
        "default",
        "dependencies",
        "description",
        "enum",
        "example",
        "exclusiveMaximum",
        "exclusiveMinimum",
        "externalDocs",
        "format",
        "id",
        "items",
        "maxItems",
        "maxLength",
        "maxProperties",
        "maximum",
        "minItems",
        "minLength",
        "minProperties",
        "minimum",
        "multipleOf",
        "nullable",
        "pattern",
        "required",
        "title",
        "type",
        "uniqueItems",
        "x_kubernetes_embedded_resource",
        "x_kubernetes_int_or_string",
        "x_kubernetes_list_map_keys",
        "x_kubernetes_list_type",
        "x_kubernetes_map_type",
        "x_kubernetes_preserve_unknown_fields",
        "x_kubernetes_validations",
    ]
    required_props: List[str] = []

    @property
    def S_ref(self) -> Optional[str]:
        return self._S_ref

    @property
    def S_schema(self) -> Optional[str]:
        return self._S_schema

    @property
    def additionalItems(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrBool
    ]:
        return self._additionalItems

    @property
    def additionalProperties(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrBool
    ]:
        return self._additionalProperties

    @property
    def default(
        self,
    ) -> Optional[io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSON]:
        return self._default

    @property
    def dependencies(
        self,
    ) -> Optional[
        Dict[
            str,
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrStringArray,
        ]
    ]:
        return self._dependencies

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def enum(
        self,
    ) -> Optional[
        List[io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSON]
    ]:
        return self._enum

    @property
    def example(
        self,
    ) -> Optional[io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSON]:
        return self._example

    @property
    def exclusiveMaximum(self) -> Optional[bool]:
        return self._exclusiveMaximum

    @property
    def exclusiveMinimum(self) -> Optional[bool]:
        return self._exclusiveMinimum

    @property
    def externalDocs(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ExternalDocumentation
    ]:
        return self._externalDocs

    @property
    def format(self) -> Optional[str]:
        return self._format

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def items(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrArray
    ]:
        return self._items

    @property
    def maxItems(self) -> Optional[int]:
        return self._maxItems

    @property
    def maxLength(self) -> Optional[int]:
        return self._maxLength

    @property
    def maxProperties(self) -> Optional[int]:
        return self._maxProperties

    @property
    def maximum(self) -> Optional[float]:
        return self._maximum

    @property
    def minItems(self) -> Optional[int]:
        return self._minItems

    @property
    def minLength(self) -> Optional[int]:
        return self._minLength

    @property
    def minProperties(self) -> Optional[int]:
        return self._minProperties

    @property
    def minimum(self) -> Optional[float]:
        return self._minimum

    @property
    def multipleOf(self) -> Optional[float]:
        return self._multipleOf

    @property
    def nullable(self) -> Optional[bool]:
        return self._nullable

    @property
    def pattern(self) -> Optional[str]:
        return self._pattern

    @property
    def required(self) -> Optional[List[str]]:
        return self._required

    @property
    def title(self) -> Optional[str]:
        return self._title

    @property
    def type(self) -> Optional[str]:
        return self._type

    @property
    def uniqueItems(self) -> Optional[bool]:
        return self._uniqueItems

    @property
    def x_kubernetes_embedded_resource(self) -> Optional[bool]:
        return self._x_kubernetes_embedded_resource

    @property
    def x_kubernetes_int_or_string(self) -> Optional[bool]:
        return self._x_kubernetes_int_or_string

    @property
    def x_kubernetes_list_map_keys(self) -> Optional[List[str]]:
        return self._x_kubernetes_list_map_keys

    @property
    def x_kubernetes_list_type(self) -> Optional[str]:
        return self._x_kubernetes_list_type

    @property
    def x_kubernetes_map_type(self) -> Optional[str]:
        return self._x_kubernetes_map_type

    @property
    def x_kubernetes_preserve_unknown_fields(self) -> Optional[bool]:
        return self._x_kubernetes_preserve_unknown_fields

    @property
    def x_kubernetes_validations(
        self,
    ) -> Optional[
        List[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ValidationRule
        ]
    ]:
        return self._x_kubernetes_validations

    def __init__(
        self,
        S_ref: Optional[str] = None,
        S_schema: Optional[str] = None,
        additionalItems: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrBool
        ] = None,
        additionalProperties: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrBool
        ] = None,
        default: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSON
        ] = None,
        dependencies: Optional[
            Dict[
                str,
                io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrStringArray,
            ]
        ] = None,
        description: Optional[str] = None,
        enum: Optional[
            List[io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSON]
        ] = None,
        example: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSON
        ] = None,
        exclusiveMaximum: Optional[bool] = None,
        exclusiveMinimum: Optional[bool] = None,
        externalDocs: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ExternalDocumentation
        ] = None,
        format: Optional[str] = None,
        id: Optional[str] = None,
        items: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrArray
        ] = None,
        maxItems: Optional[int] = None,
        maxLength: Optional[int] = None,
        maxProperties: Optional[int] = None,
        maximum: Optional[float] = None,
        minItems: Optional[int] = None,
        minLength: Optional[int] = None,
        minProperties: Optional[int] = None,
        minimum: Optional[float] = None,
        multipleOf: Optional[float] = None,
        nullable: Optional[bool] = None,
        pattern: Optional[str] = None,
        required: Optional[List[str]] = None,
        title: Optional[str] = None,
        type: Optional[str] = None,
        uniqueItems: Optional[bool] = None,
        x_kubernetes_embedded_resource: Optional[bool] = None,
        x_kubernetes_int_or_string: Optional[bool] = None,
        x_kubernetes_list_map_keys: Optional[List[str]] = None,
        x_kubernetes_list_type: Optional[str] = None,
        x_kubernetes_map_type: Optional[str] = None,
        x_kubernetes_preserve_unknown_fields: Optional[bool] = None,
        x_kubernetes_validations: Optional[
            List[
                io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ValidationRule
            ]
        ] = None,
    ):
        super().__init__()
        if S_ref is not None:
            self._S_ref = S_ref
        if S_schema is not None:
            self._S_schema = S_schema
        if additionalItems is not None:
            self._additionalItems = additionalItems
        if additionalProperties is not None:
            self._additionalProperties = additionalProperties
        if default is not None:
            self._default = default
        if dependencies is not None:
            self._dependencies = dependencies
        if description is not None:
            self._description = description
        if enum is not None:
            self._enum = enum
        if example is not None:
            self._example = example
        if exclusiveMaximum is not None:
            self._exclusiveMaximum = exclusiveMaximum
        if exclusiveMinimum is not None:
            self._exclusiveMinimum = exclusiveMinimum
        if externalDocs is not None:
            self._externalDocs = externalDocs
        if format is not None:
            self._format = format
        if id is not None:
            self._id = id
        if items is not None:
            self._items = items
        if maxItems is not None:
            self._maxItems = maxItems
        if maxLength is not None:
            self._maxLength = maxLength
        if maxProperties is not None:
            self._maxProperties = maxProperties
        if maximum is not None:
            self._maximum = maximum
        if minItems is not None:
            self._minItems = minItems
        if minLength is not None:
            self._minLength = minLength
        if minProperties is not None:
            self._minProperties = minProperties
        if minimum is not None:
            self._minimum = minimum
        if multipleOf is not None:
            self._multipleOf = multipleOf
        if nullable is not None:
            self._nullable = nullable
        if pattern is not None:
            self._pattern = pattern
        if required is not None:
            self._required = required
        if title is not None:
            self._title = title
        if type is not None:
            self._type = type
        if uniqueItems is not None:
            self._uniqueItems = uniqueItems
        if x_kubernetes_embedded_resource is not None:
            self._x_kubernetes_embedded_resource = x_kubernetes_embedded_resource
        if x_kubernetes_int_or_string is not None:
            self._x_kubernetes_int_or_string = x_kubernetes_int_or_string
        if x_kubernetes_list_map_keys is not None:
            self._x_kubernetes_list_map_keys = x_kubernetes_list_map_keys
        if x_kubernetes_list_type is not None:
            self._x_kubernetes_list_type = x_kubernetes_list_type
        if x_kubernetes_map_type is not None:
            self._x_kubernetes_map_type = x_kubernetes_map_type
        if x_kubernetes_preserve_unknown_fields is not None:
            self._x_kubernetes_preserve_unknown_fields = (
                x_kubernetes_preserve_unknown_fields
            )
        if x_kubernetes_validations is not None:
            self._x_kubernetes_validations = x_kubernetes_validations


class io__k8s__apimachinery__pkg__apis__meta__v1__APIGroup(K8STemplatable):
    """APIGroup contains the name, the supported versions, and the preferred version of a group."""

    apiVersion: str = "v1"
    kind: str = "APIGroup"

    props: List[str] = [
        "apiVersion",
        "kind",
        "name",
        "preferredVersion",
        "serverAddressByClientCIDRs",
        "versions",
    ]
    required_props: List[str] = ["name", "versions"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def preferredVersion(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__GroupVersionForDiscovery]:
        return self._preferredVersion

    @property
    def serverAddressByClientCIDRs(
        self,
    ) -> Optional[
        List[io__k8s__apimachinery__pkg__apis__meta__v1__ServerAddressByClientCIDR]
    ]:
        return self._serverAddressByClientCIDRs

    @property
    def versions(
        self,
    ) -> List[io__k8s__apimachinery__pkg__apis__meta__v1__GroupVersionForDiscovery]:
        return self._versions

    def __init__(
        self,
        name: str,
        versions: List[
            io__k8s__apimachinery__pkg__apis__meta__v1__GroupVersionForDiscovery
        ],
        preferredVersion: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__GroupVersionForDiscovery
        ] = None,
        serverAddressByClientCIDRs: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__ServerAddressByClientCIDR]
        ] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if versions is not None:
            self._versions = versions
        if preferredVersion is not None:
            self._preferredVersion = preferredVersion
        if serverAddressByClientCIDRs is not None:
            self._serverAddressByClientCIDRs = serverAddressByClientCIDRs


class io__k8s__apimachinery__pkg__apis__meta__v1__APIGroupList(K8STemplatable):
    """APIGroupList is a list of APIGroup, to allow clients to discover the API at /apis."""

    apiVersion: str = "v1"
    kind: str = "APIGroupList"

    props: List[str] = ["apiVersion", "groups", "kind"]
    required_props: List[str] = ["groups"]

    @property
    def groups(self) -> List[io__k8s__apimachinery__pkg__apis__meta__v1__APIGroup]:
        return self._groups

    def __init__(
        self, groups: List[io__k8s__apimachinery__pkg__apis__meta__v1__APIGroup]
    ):
        super().__init__()
        if groups is not None:
            self._groups = groups


class io__k8s__apimachinery__pkg__apis__meta__v1__APIVersions(K8STemplatable):
    """APIVersions lists the versions that are available, to allow clients to discover the API at /api, which is the root path of the legacy v1 API."""

    apiVersion: str = "v1"
    kind: str = "APIVersions"

    props: List[str] = ["apiVersion", "kind", "serverAddressByClientCIDRs", "versions"]
    required_props: List[str] = ["versions", "serverAddressByClientCIDRs"]

    @property
    def serverAddressByClientCIDRs(
        self,
    ) -> List[io__k8s__apimachinery__pkg__apis__meta__v1__ServerAddressByClientCIDR]:
        return self._serverAddressByClientCIDRs

    @property
    def versions(self) -> List[str]:
        return self._versions

    def __init__(
        self,
        serverAddressByClientCIDRs: List[
            io__k8s__apimachinery__pkg__apis__meta__v1__ServerAddressByClientCIDR
        ],
        versions: List[str],
    ):
        super().__init__()
        if serverAddressByClientCIDRs is not None:
            self._serverAddressByClientCIDRs = serverAddressByClientCIDRs
        if versions is not None:
            self._versions = versions


class io__k8s__apimachinery__pkg__apis__meta__v1__Condition(K8STemplatable):
    """Condition contains details for one aspect of the current state of this API Resource."""

    props: List[str] = [
        "lastTransitionTime",
        "message",
        "observedGeneration",
        "reason",
        "status",
        "type",
    ]
    required_props: List[str] = [
        "type",
        "status",
        "lastTransitionTime",
        "reason",
        "message",
    ]

    @property
    def lastTransitionTime(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__Time:
        return self._lastTransitionTime

    @property
    def message(self) -> str:
        return self._message

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def status(self) -> str:
        return self._status

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        lastTransitionTime: io__k8s__apimachinery__pkg__apis__meta__v1__Time,
        message: str,
        reason: str,
        status: str,
        type: str,
        observedGeneration: Optional[int] = None,
    ):
        super().__init__()
        if lastTransitionTime is not None:
            self._lastTransitionTime = lastTransitionTime
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason
        if status is not None:
            self._status = status
        if type is not None:
            self._type = type
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration


class io__k8s__apimachinery__pkg__apis__meta__v1__DeleteOptions(K8STemplatable):
    """DeleteOptions may be provided when deleting an API object."""

    apiVersion: str = "v1"
    kind: str = "DeleteOptions"

    props: List[str] = [
        "apiVersion",
        "dryRun",
        "gracePeriodSeconds",
        "kind",
        "orphanDependents",
        "preconditions",
        "propagationPolicy",
    ]
    required_props: List[str] = []

    @property
    def dryRun(self) -> Optional[List[str]]:
        return self._dryRun

    @property
    def gracePeriodSeconds(self) -> Optional[int]:
        return self._gracePeriodSeconds

    @property
    def orphanDependents(self) -> Optional[bool]:
        return self._orphanDependents

    @property
    def preconditions(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Preconditions]:
        return self._preconditions

    @property
    def propagationPolicy(self) -> Optional[str]:
        return self._propagationPolicy

    def __init__(
        self,
        dryRun: Optional[List[str]] = None,
        gracePeriodSeconds: Optional[int] = None,
        orphanDependents: Optional[bool] = None,
        preconditions: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Preconditions
        ] = None,
        propagationPolicy: Optional[str] = None,
    ):
        super().__init__()
        if dryRun is not None:
            self._dryRun = dryRun
        if gracePeriodSeconds is not None:
            self._gracePeriodSeconds = gracePeriodSeconds
        if orphanDependents is not None:
            self._orphanDependents = orphanDependents
        if preconditions is not None:
            self._preconditions = preconditions
        if propagationPolicy is not None:
            self._propagationPolicy = propagationPolicy


class io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector(K8STemplatable):
    """A label selector is a label query over a set of resources. The result of matchLabels and matchExpressions are ANDed. An empty label selector matches all objects. A null label selector matches no objects."""

    props: List[str] = ["matchExpressions", "matchLabels"]
    required_props: List[str] = []

    @property
    def matchExpressions(
        self,
    ) -> Optional[
        List[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelectorRequirement]
    ]:
        return self._matchExpressions

    @property
    def matchLabels(self) -> Optional[Dict[str, str]]:
        return self._matchLabels

    def __init__(
        self,
        matchExpressions: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelectorRequirement]
        ] = None,
        matchLabels: Optional[Dict[str, str]] = None,
    ):
        super().__init__()
        if matchExpressions is not None:
            self._matchExpressions = matchExpressions
        if matchLabels is not None:
            self._matchLabels = matchLabels


class io__k8s__apimachinery__pkg__apis__meta__v1__ManagedFieldsEntry(K8STemplatable):
    """ManagedFieldsEntry is a workflow-id, a FieldSet and the group version of the resource that the fieldset applies to."""

    props: List[str] = [
        "apiVersion",
        "fieldsType",
        "fieldsV1",
        "manager",
        "operation",
        "subresource",
        "time",
    ]
    required_props: List[str] = []

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @property
    def fieldsType(self) -> Optional[str]:
        return self._fieldsType

    @property
    def fieldsV1(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__FieldsV1]:
        return self._fieldsV1

    @property
    def manager(self) -> Optional[str]:
        return self._manager

    @property
    def operation(self) -> Optional[str]:
        return self._operation

    @property
    def subresource(self) -> Optional[str]:
        return self._subresource

    @property
    def time(self) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._time

    def __init__(
        self,
        apiVersion: Optional[str] = None,
        fieldsType: Optional[str] = None,
        fieldsV1: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__FieldsV1] = None,
        manager: Optional[str] = None,
        operation: Optional[str] = None,
        subresource: Optional[str] = None,
        time: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time] = None,
    ):
        super().__init__()
        if apiVersion is not None:
            self._apiVersion = apiVersion
        if fieldsType is not None:
            self._fieldsType = fieldsType
        if fieldsV1 is not None:
            self._fieldsV1 = fieldsV1
        if manager is not None:
            self._manager = manager
        if operation is not None:
            self._operation = operation
        if subresource is not None:
            self._subresource = subresource
        if time is not None:
            self._time = time


class io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta(K8STemplatable):
    """ObjectMeta is metadata that all persisted resources must have, which includes all objects users must create."""

    props: List[str] = [
        "annotations",
        "clusterName",
        "creationTimestamp",
        "deletionGracePeriodSeconds",
        "deletionTimestamp",
        "finalizers",
        "generateName",
        "generation",
        "labels",
        "managedFields",
        "name",
        "namespace",
        "ownerReferences",
        "resourceVersion",
        "selfLink",
        "uid",
    ]
    required_props: List[str] = []

    @property
    def annotations(self) -> Optional[Dict[str, str]]:
        return self._annotations

    @property
    def clusterName(self) -> Optional[str]:
        return self._clusterName

    @property
    def creationTimestamp(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._creationTimestamp

    @property
    def deletionGracePeriodSeconds(self) -> Optional[int]:
        return self._deletionGracePeriodSeconds

    @property
    def deletionTimestamp(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._deletionTimestamp

    @property
    def finalizers(self) -> Optional[List[str]]:
        return self._finalizers

    @property
    def generateName(self) -> Optional[str]:
        return self._generateName

    @property
    def generation(self) -> Optional[int]:
        return self._generation

    @property
    def labels(self) -> Optional[Dict[str, str]]:
        return self._labels

    @property
    def managedFields(
        self,
    ) -> Optional[List[io__k8s__apimachinery__pkg__apis__meta__v1__ManagedFieldsEntry]]:
        return self._managedFields

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    @property
    def ownerReferences(
        self,
    ) -> Optional[List[io__k8s__apimachinery__pkg__apis__meta__v1__OwnerReference]]:
        return self._ownerReferences

    @property
    def resourceVersion(self) -> Optional[str]:
        return self._resourceVersion

    @property
    def selfLink(self) -> Optional[str]:
        return self._selfLink

    @property
    def uid(self) -> Optional[str]:
        return self._uid

    def __init__(
        self,
        annotations: Optional[Dict[str, str]] = None,
        clusterName: Optional[str] = None,
        creationTimestamp: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        deletionGracePeriodSeconds: Optional[int] = None,
        deletionTimestamp: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        finalizers: Optional[List[str]] = None,
        generateName: Optional[str] = None,
        generation: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None,
        managedFields: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__ManagedFieldsEntry]
        ] = None,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        ownerReferences: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__OwnerReference]
        ] = None,
        resourceVersion: Optional[str] = None,
        selfLink: Optional[str] = None,
        uid: Optional[str] = None,
    ):
        super().__init__()
        if annotations is not None:
            self._annotations = annotations
        if clusterName is not None:
            self._clusterName = clusterName
        if creationTimestamp is not None:
            self._creationTimestamp = creationTimestamp
        if deletionGracePeriodSeconds is not None:
            self._deletionGracePeriodSeconds = deletionGracePeriodSeconds
        if deletionTimestamp is not None:
            self._deletionTimestamp = deletionTimestamp
        if finalizers is not None:
            self._finalizers = finalizers
        if generateName is not None:
            self._generateName = generateName
        if generation is not None:
            self._generation = generation
        if labels is not None:
            self._labels = labels
        if managedFields is not None:
            self._managedFields = managedFields
        if name is not None:
            self._name = name
        if namespace is not None:
            self._namespace = namespace
        if ownerReferences is not None:
            self._ownerReferences = ownerReferences
        if resourceVersion is not None:
            self._resourceVersion = resourceVersion
        if selfLink is not None:
            self._selfLink = selfLink
        if uid is not None:
            self._uid = uid


class io__k8s__apimachinery__pkg__apis__meta__v1__Status(K8STemplatable):
    """Status is a return value for calls that don't return other objects."""

    apiVersion: str = "v1"
    kind: str = "Status"

    props: List[str] = [
        "apiVersion",
        "code",
        "details",
        "kind",
        "message",
        "metadata",
        "reason",
        "status",
    ]
    required_props: List[str] = []

    @property
    def code(self) -> Optional[int]:
        return self._code

    @property
    def details(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__StatusDetails]:
        return self._details

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def status(self) -> Optional[str]:
        return self._status

    def __init__(
        self,
        code: Optional[int] = None,
        details: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__StatusDetails
        ] = None,
        message: Optional[str] = None,
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
        reason: Optional[str] = None,
        status: Optional[str] = None,
    ):
        super().__init__()
        if code is not None:
            self._code = code
        if details is not None:
            self._details = details
        if message is not None:
            self._message = message
        if metadata is not None:
            self._metadata = metadata
        if reason is not None:
            self._reason = reason
        if status is not None:
            self._status = status


class io__k8s__apimachinery__pkg__apis__meta__v1__WatchEvent(K8STemplatable):
    """Event represents a single event to a watched resource."""

    apiVersion: str = "v1"
    kind: str = "WatchEvent"

    props: List[str] = ["object", "type"]
    required_props: List[str] = ["type", "object"]

    @property
    def object(self) -> io__k8s__apimachinery__pkg__runtime__RawExtension:
        return self._object

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self, object: io__k8s__apimachinery__pkg__runtime__RawExtension, type: str
    ):
        super().__init__()
        if object is not None:
            self._object = object
        if type is not None:
            self._type = type


class io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceSpec(
    K8STemplatable
):
    """APIServiceSpec contains information for locating and communicating with a server. Only https is supported, though you are able to disable certificate verification."""

    props: List[str] = [
        "caBundle",
        "group",
        "groupPriorityMinimum",
        "insecureSkipTLSVerify",
        "service",
        "version",
        "versionPriority",
    ]
    required_props: List[str] = ["groupPriorityMinimum", "versionPriority"]

    @property
    def caBundle(self) -> Optional[str]:
        return self._caBundle

    @property
    def group(self) -> Optional[str]:
        return self._group

    @property
    def groupPriorityMinimum(self) -> int:
        return self._groupPriorityMinimum

    @property
    def insecureSkipTLSVerify(self) -> Optional[bool]:
        return self._insecureSkipTLSVerify

    @property
    def service(
        self,
    ) -> Optional[
        io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__ServiceReference
    ]:
        return self._service

    @property
    def version(self) -> Optional[str]:
        return self._version

    @property
    def versionPriority(self) -> int:
        return self._versionPriority

    def __init__(
        self,
        groupPriorityMinimum: int,
        versionPriority: int,
        caBundle: Optional[str] = None,
        group: Optional[str] = None,
        insecureSkipTLSVerify: Optional[bool] = None,
        service: Optional[
            io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__ServiceReference
        ] = None,
        version: Optional[str] = None,
    ):
        super().__init__()
        if groupPriorityMinimum is not None:
            self._groupPriorityMinimum = groupPriorityMinimum
        if versionPriority is not None:
            self._versionPriority = versionPriority
        if caBundle is not None:
            self._caBundle = caBundle
        if group is not None:
            self._group = group
        if insecureSkipTLSVerify is not None:
            self._insecureSkipTLSVerify = insecureSkipTLSVerify
        if service is not None:
            self._service = service
        if version is not None:
            self._version = version


class io__k8s__api__admissionregistration__v1__MutatingWebhook(K8STemplatable):
    """MutatingWebhook describes an admission webhook and the resources and operations it applies to."""

    props: List[str] = [
        "admissionReviewVersions",
        "clientConfig",
        "failurePolicy",
        "matchPolicy",
        "name",
        "namespaceSelector",
        "objectSelector",
        "reinvocationPolicy",
        "rules",
        "sideEffects",
        "timeoutSeconds",
    ]
    required_props: List[str] = [
        "name",
        "clientConfig",
        "sideEffects",
        "admissionReviewVersions",
    ]

    @property
    def admissionReviewVersions(self) -> List[str]:
        return self._admissionReviewVersions

    @property
    def clientConfig(
        self,
    ) -> io__k8s__api__admissionregistration__v1__WebhookClientConfig:
        return self._clientConfig

    @property
    def failurePolicy(self) -> Optional[str]:
        return self._failurePolicy

    @property
    def matchPolicy(self) -> Optional[str]:
        return self._matchPolicy

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespaceSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._namespaceSelector

    @property
    def objectSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._objectSelector

    @property
    def reinvocationPolicy(self) -> Optional[str]:
        return self._reinvocationPolicy

    @property
    def rules(
        self,
    ) -> Optional[List[io__k8s__api__admissionregistration__v1__RuleWithOperations]]:
        return self._rules

    @property
    def sideEffects(self) -> str:
        return self._sideEffects

    @property
    def timeoutSeconds(self) -> Optional[int]:
        return self._timeoutSeconds

    def __init__(
        self,
        admissionReviewVersions: List[str],
        clientConfig: io__k8s__api__admissionregistration__v1__WebhookClientConfig,
        name: str,
        sideEffects: str,
        failurePolicy: Optional[str] = None,
        matchPolicy: Optional[str] = None,
        namespaceSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        objectSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        reinvocationPolicy: Optional[str] = None,
        rules: Optional[
            List[io__k8s__api__admissionregistration__v1__RuleWithOperations]
        ] = None,
        timeoutSeconds: Optional[int] = None,
    ):
        super().__init__()
        if admissionReviewVersions is not None:
            self._admissionReviewVersions = admissionReviewVersions
        if clientConfig is not None:
            self._clientConfig = clientConfig
        if name is not None:
            self._name = name
        if sideEffects is not None:
            self._sideEffects = sideEffects
        if failurePolicy is not None:
            self._failurePolicy = failurePolicy
        if matchPolicy is not None:
            self._matchPolicy = matchPolicy
        if namespaceSelector is not None:
            self._namespaceSelector = namespaceSelector
        if objectSelector is not None:
            self._objectSelector = objectSelector
        if reinvocationPolicy is not None:
            self._reinvocationPolicy = reinvocationPolicy
        if rules is not None:
            self._rules = rules
        if timeoutSeconds is not None:
            self._timeoutSeconds = timeoutSeconds


class io__k8s__api__admissionregistration__v1__MutatingWebhookConfiguration(
    K8STemplatable
):
    """MutatingWebhookConfiguration describes the configuration of and admission webhook that accept or reject and may change the object."""

    apiVersion: str = "admissionregistration.k8s.io/v1"
    kind: str = "MutatingWebhookConfiguration"

    props: List[str] = ["apiVersion", "kind", "metadata", "webhooks"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def webhooks(
        self,
    ) -> Optional[List[io__k8s__api__admissionregistration__v1__MutatingWebhook]]:
        return self._webhooks

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        webhooks: Optional[
            List[io__k8s__api__admissionregistration__v1__MutatingWebhook]
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if webhooks is not None:
            self._webhooks = webhooks


class io__k8s__api__admissionregistration__v1__MutatingWebhookConfigurationList(
    K8STemplatable
):
    """MutatingWebhookConfigurationList is a list of MutatingWebhookConfiguration."""

    apiVersion: str = "admissionregistration.k8s.io/v1"
    kind: str = "MutatingWebhookConfigurationList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(
        self,
    ) -> List[io__k8s__api__admissionregistration__v1__MutatingWebhookConfiguration]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[
            io__k8s__api__admissionregistration__v1__MutatingWebhookConfiguration
        ],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__admissionregistration__v1__ValidatingWebhook(K8STemplatable):
    """ValidatingWebhook describes an admission webhook and the resources and operations it applies to."""

    props: List[str] = [
        "admissionReviewVersions",
        "clientConfig",
        "failurePolicy",
        "matchPolicy",
        "name",
        "namespaceSelector",
        "objectSelector",
        "rules",
        "sideEffects",
        "timeoutSeconds",
    ]
    required_props: List[str] = [
        "name",
        "clientConfig",
        "sideEffects",
        "admissionReviewVersions",
    ]

    @property
    def admissionReviewVersions(self) -> List[str]:
        return self._admissionReviewVersions

    @property
    def clientConfig(
        self,
    ) -> io__k8s__api__admissionregistration__v1__WebhookClientConfig:
        return self._clientConfig

    @property
    def failurePolicy(self) -> Optional[str]:
        return self._failurePolicy

    @property
    def matchPolicy(self) -> Optional[str]:
        return self._matchPolicy

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespaceSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._namespaceSelector

    @property
    def objectSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._objectSelector

    @property
    def rules(
        self,
    ) -> Optional[List[io__k8s__api__admissionregistration__v1__RuleWithOperations]]:
        return self._rules

    @property
    def sideEffects(self) -> str:
        return self._sideEffects

    @property
    def timeoutSeconds(self) -> Optional[int]:
        return self._timeoutSeconds

    def __init__(
        self,
        admissionReviewVersions: List[str],
        clientConfig: io__k8s__api__admissionregistration__v1__WebhookClientConfig,
        name: str,
        sideEffects: str,
        failurePolicy: Optional[str] = None,
        matchPolicy: Optional[str] = None,
        namespaceSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        objectSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        rules: Optional[
            List[io__k8s__api__admissionregistration__v1__RuleWithOperations]
        ] = None,
        timeoutSeconds: Optional[int] = None,
    ):
        super().__init__()
        if admissionReviewVersions is not None:
            self._admissionReviewVersions = admissionReviewVersions
        if clientConfig is not None:
            self._clientConfig = clientConfig
        if name is not None:
            self._name = name
        if sideEffects is not None:
            self._sideEffects = sideEffects
        if failurePolicy is not None:
            self._failurePolicy = failurePolicy
        if matchPolicy is not None:
            self._matchPolicy = matchPolicy
        if namespaceSelector is not None:
            self._namespaceSelector = namespaceSelector
        if objectSelector is not None:
            self._objectSelector = objectSelector
        if rules is not None:
            self._rules = rules
        if timeoutSeconds is not None:
            self._timeoutSeconds = timeoutSeconds


class io__k8s__api__admissionregistration__v1__ValidatingWebhookConfiguration(
    K8STemplatable
):
    """ValidatingWebhookConfiguration describes the configuration of and admission webhook that accept or reject and object without changing it."""

    apiVersion: str = "admissionregistration.k8s.io/v1"
    kind: str = "ValidatingWebhookConfiguration"

    props: List[str] = ["apiVersion", "kind", "metadata", "webhooks"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def webhooks(
        self,
    ) -> Optional[List[io__k8s__api__admissionregistration__v1__ValidatingWebhook]]:
        return self._webhooks

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        webhooks: Optional[
            List[io__k8s__api__admissionregistration__v1__ValidatingWebhook]
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if webhooks is not None:
            self._webhooks = webhooks


class io__k8s__api__admissionregistration__v1__ValidatingWebhookConfigurationList(
    K8STemplatable
):
    """ValidatingWebhookConfigurationList is a list of ValidatingWebhookConfiguration."""

    apiVersion: str = "admissionregistration.k8s.io/v1"
    kind: str = "ValidatingWebhookConfigurationList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(
        self,
    ) -> List[io__k8s__api__admissionregistration__v1__ValidatingWebhookConfiguration]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[
            io__k8s__api__admissionregistration__v1__ValidatingWebhookConfiguration
        ],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apiserverinternal__v1alpha1__StorageVersion(K8STemplatable):
    """Storage version of a specific resource."""

    apiVersion: str = "internal.apiserver.k8s.io/v1alpha1"
    kind: str = "StorageVersion"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec", "status"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__apiserverinternal__v1alpha1__StorageVersionSpec:
        return self._spec

    @property
    def status(self) -> io__k8s__api__apiserverinternal__v1alpha1__StorageVersionStatus:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__apiserverinternal__v1alpha1__StorageVersionSpec,
        status: io__k8s__api__apiserverinternal__v1alpha1__StorageVersionStatus,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apiserverinternal__v1alpha1__StorageVersionList(K8STemplatable):
    """A list of StorageVersions."""

    apiVersion: str = "internal.apiserver.k8s.io/v1alpha1"
    kind: str = "StorageVersionList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__apiserverinternal__v1alpha1__StorageVersion]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__apiserverinternal__v1alpha1__StorageVersion],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apps__v1__ControllerRevision(K8STemplatable):
    """ControllerRevision implements an immutable snapshot of state data. Clients are responsible for serializing and deserializing the objects that contain their internal state. Once a ControllerRevision has been successfully created, it can not be updated. The API Server will fail validation of all requests that attempt to mutate the Data field. ControllerRevisions may, however, be deleted. Note that, due to its use by both the DaemonSet and StatefulSet controllers for update and rollback, this object is beta. However, it may be subject to name and representation changes in future releases, and clients should not depend on its stability. It is primarily for internal use by controllers."""

    apiVersion: str = "apps/v1"
    kind: str = "ControllerRevision"

    props: List[str] = ["apiVersion", "data", "kind", "metadata", "revision"]
    required_props: List[str] = ["revision"]

    @property
    def data(self) -> Optional[io__k8s__apimachinery__pkg__runtime__RawExtension]:
        return self._data

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def revision(self) -> int:
        return self._revision

    def __init__(
        self,
        revision: int,
        data: Optional[io__k8s__apimachinery__pkg__runtime__RawExtension] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if revision is not None:
            self._revision = revision
        if data is not None:
            self._data = data
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apps__v1__ControllerRevisionList(K8STemplatable):
    """ControllerRevisionList is a resource containing a list of ControllerRevision objects."""

    apiVersion: str = "apps/v1"
    kind: str = "ControllerRevisionList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__apps__v1__ControllerRevision]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__apps__v1__ControllerRevision],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apps__v1__DaemonSetUpdateStrategy(K8STemplatable):
    """DaemonSetUpdateStrategy is a struct used to control the update strategy for a DaemonSet."""

    props: List[str] = ["rollingUpdate", "type"]
    required_props: List[str] = []

    @property
    def rollingUpdate(self) -> Optional[io__k8s__api__apps__v1__RollingUpdateDaemonSet]:
        return self._rollingUpdate

    @property
    def type(self) -> Optional[Literal["OnDelete", "RollingUpdate"]]:
        return self._type

    def __init__(
        self,
        rollingUpdate: Optional[io__k8s__api__apps__v1__RollingUpdateDaemonSet] = None,
        type: Optional[Literal["OnDelete", "RollingUpdate"]] = None,
    ):
        super().__init__()
        if rollingUpdate is not None:
            self._rollingUpdate = rollingUpdate
        if type is not None:
            self._type = type


class io__k8s__api__apps__v1__DeploymentStrategy(K8STemplatable):
    """DeploymentStrategy describes how to replace existing pods with new ones."""

    props: List[str] = ["rollingUpdate", "type"]
    required_props: List[str] = []

    @property
    def rollingUpdate(
        self,
    ) -> Optional[io__k8s__api__apps__v1__RollingUpdateDeployment]:
        return self._rollingUpdate

    @property
    def type(self) -> Optional[Literal["Recreate", "RollingUpdate"]]:
        return self._type

    def __init__(
        self,
        rollingUpdate: Optional[io__k8s__api__apps__v1__RollingUpdateDeployment] = None,
        type: Optional[Literal["Recreate", "RollingUpdate"]] = None,
    ):
        super().__init__()
        if rollingUpdate is not None:
            self._rollingUpdate = rollingUpdate
        if type is not None:
            self._type = type


class io__k8s__api__authentication__v1__TokenRequest(K8STemplatable):
    """TokenRequest requests a token for a given service account."""

    apiVersion: str = "authentication.k8s.io/v1"
    kind: str = "TokenRequest"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__authentication__v1__TokenRequestSpec:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__authentication__v1__TokenRequestStatus]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__authentication__v1__TokenRequestSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[io__k8s__api__authentication__v1__TokenRequestStatus] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__api__authentication__v1__TokenReview(K8STemplatable):
    """TokenReview attempts to authenticate a token to a known user. Note: TokenReview requests may be cached by the webhook token authenticator plugin in the kube-apiserver."""

    apiVersion: str = "authentication.k8s.io/v1"
    kind: str = "TokenReview"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__authentication__v1__TokenReviewSpec:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__authentication__v1__TokenReviewStatus]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__authentication__v1__TokenReviewSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[io__k8s__api__authentication__v1__TokenReviewStatus] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__api__authorization__v1__LocalSubjectAccessReview(K8STemplatable):
    """LocalSubjectAccessReview checks whether or not a user or group can perform an action in a given namespace. Having a namespace scoped resource makes it much easier to grant namespace scoped policy that includes permissions checking."""

    apiVersion: str = "authorization.k8s.io/v1"
    kind: str = "LocalSubjectAccessReview"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__authorization__v1__SubjectAccessReviewSpec:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__authorization__v1__SubjectAccessReviewStatus]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__authorization__v1__SubjectAccessReviewSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[
            io__k8s__api__authorization__v1__SubjectAccessReviewStatus
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__api__authorization__v1__SelfSubjectAccessReview(K8STemplatable):
    """SelfSubjectAccessReview checks whether or the current user can perform an action.  Not filling in a spec.namespace means "in all namespaces".  Self is a special case, because users should always be able to check whether they can perform an action"""

    apiVersion: str = "authorization.k8s.io/v1"
    kind: str = "SelfSubjectAccessReview"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__authorization__v1__SelfSubjectAccessReviewSpec:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__authorization__v1__SubjectAccessReviewStatus]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__authorization__v1__SelfSubjectAccessReviewSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[
            io__k8s__api__authorization__v1__SubjectAccessReviewStatus
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__api__authorization__v1__SelfSubjectRulesReview(K8STemplatable):
    """SelfSubjectRulesReview enumerates the set of actions the current user can perform within a namespace. The returned list of actions may be incomplete depending on the server's authorization mode, and any errors experienced during the evaluation. SelfSubjectRulesReview should be used by UIs to show/hide actions, or to quickly let an end user reason about their permissions. It should NOT Be used by external systems to drive authorization decisions as this raises confused deputy, cache lifetime/revocation, and correctness concerns. SubjectAccessReview, and LocalAccessReview are the correct way to defer authorization decisions to the API server."""

    apiVersion: str = "authorization.k8s.io/v1"
    kind: str = "SelfSubjectRulesReview"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__authorization__v1__SelfSubjectRulesReviewSpec:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__authorization__v1__SubjectRulesReviewStatus]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__authorization__v1__SelfSubjectRulesReviewSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[
            io__k8s__api__authorization__v1__SubjectRulesReviewStatus
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__api__authorization__v1__SubjectAccessReview(K8STemplatable):
    """SubjectAccessReview checks whether or not a user or group can perform an action."""

    apiVersion: str = "authorization.k8s.io/v1"
    kind: str = "SubjectAccessReview"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__authorization__v1__SubjectAccessReviewSpec:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__authorization__v1__SubjectAccessReviewStatus]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__authorization__v1__SubjectAccessReviewSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[
            io__k8s__api__authorization__v1__SubjectAccessReviewStatus
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__api__autoscaling__v1__HorizontalPodAutoscaler(K8STemplatable):
    """configuration of a horizontal pod autoscaler."""

    apiVersion: str = "autoscaling/v1"
    kind: str = "HorizontalPodAutoscaler"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v1__HorizontalPodAutoscalerSpec]:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v1__HorizontalPodAutoscalerStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[
            io__k8s__api__autoscaling__v1__HorizontalPodAutoscalerSpec
        ] = None,
        status: Optional[
            io__k8s__api__autoscaling__v1__HorizontalPodAutoscalerStatus
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__autoscaling__v1__HorizontalPodAutoscalerList(K8STemplatable):
    """list of horizontal pod autoscaler objects."""

    apiVersion: str = "autoscaling/v1"
    kind: str = "HorizontalPodAutoscalerList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__autoscaling__v1__HorizontalPodAutoscaler]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__autoscaling__v1__HorizontalPodAutoscaler],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__autoscaling__v1__Scale(K8STemplatable):
    """Scale represents a scaling request for a resource."""

    apiVersion: str = "autoscaling/v1"
    kind: str = "Scale"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__autoscaling__v1__ScaleSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__autoscaling__v1__ScaleStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__autoscaling__v1__ScaleSpec] = None,
        status: Optional[io__k8s__api__autoscaling__v1__ScaleStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__autoscaling__v2__ContainerResourceMetricSource(K8STemplatable):
    """ContainerResourceMetricSource indicates how to scale on a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  The values will be averaged together before being compared to the target.  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.  Only one "target" type should be set."""

    props: List[str] = ["container", "name", "target"]
    required_props: List[str] = ["name", "target", "container"]

    @property
    def container(self) -> str:
        return self._container

    @property
    def name(self) -> str:
        return self._name

    @property
    def target(self) -> io__k8s__api__autoscaling__v2__MetricTarget:
        return self._target

    def __init__(
        self,
        container: str,
        name: str,
        target: io__k8s__api__autoscaling__v2__MetricTarget,
    ):
        super().__init__()
        if container is not None:
            self._container = container
        if name is not None:
            self._name = name
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2__ContainerResourceMetricStatus(K8STemplatable):
    """ContainerResourceMetricStatus indicates the current value of a resource metric known to Kubernetes, as specified in requests and limits, describing a single container in each pod in the current scale target (e.g. CPU or memory).  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source."""

    props: List[str] = ["container", "current", "name"]
    required_props: List[str] = ["name", "current", "container"]

    @property
    def container(self) -> str:
        return self._container

    @property
    def current(self) -> io__k8s__api__autoscaling__v2__MetricValueStatus:
        return self._current

    @property
    def name(self) -> str:
        return self._name

    def __init__(
        self,
        container: str,
        current: io__k8s__api__autoscaling__v2__MetricValueStatus,
        name: str,
    ):
        super().__init__()
        if container is not None:
            self._container = container
        if current is not None:
            self._current = current
        if name is not None:
            self._name = name


class io__k8s__api__autoscaling__v2__MetricIdentifier(K8STemplatable):
    """MetricIdentifier defines the name and optionally selector for a metric"""

    props: List[str] = ["name", "selector"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    def __init__(
        self,
        name: str,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if selector is not None:
            self._selector = selector


class io__k8s__api__autoscaling__v2__ObjectMetricSource(K8STemplatable):
    """ObjectMetricSource indicates how to scale on a metric describing a kubernetes object (for example, hits-per-second on an Ingress object)."""

    props: List[str] = ["describedObject", "metric", "target"]
    required_props: List[str] = ["describedObject", "target", "metric"]

    @property
    def describedObject(
        self,
    ) -> io__k8s__api__autoscaling__v2__CrossVersionObjectReference:
        return self._describedObject

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2__MetricIdentifier:
        return self._metric

    @property
    def target(self) -> io__k8s__api__autoscaling__v2__MetricTarget:
        return self._target

    def __init__(
        self,
        describedObject: io__k8s__api__autoscaling__v2__CrossVersionObjectReference,
        metric: io__k8s__api__autoscaling__v2__MetricIdentifier,
        target: io__k8s__api__autoscaling__v2__MetricTarget,
    ):
        super().__init__()
        if describedObject is not None:
            self._describedObject = describedObject
        if metric is not None:
            self._metric = metric
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2__ObjectMetricStatus(K8STemplatable):
    """ObjectMetricStatus indicates the current value of a metric describing a kubernetes object (for example, hits-per-second on an Ingress object)."""

    props: List[str] = ["current", "describedObject", "metric"]
    required_props: List[str] = ["metric", "current", "describedObject"]

    @property
    def current(self) -> io__k8s__api__autoscaling__v2__MetricValueStatus:
        return self._current

    @property
    def describedObject(
        self,
    ) -> io__k8s__api__autoscaling__v2__CrossVersionObjectReference:
        return self._describedObject

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2__MetricIdentifier:
        return self._metric

    def __init__(
        self,
        current: io__k8s__api__autoscaling__v2__MetricValueStatus,
        describedObject: io__k8s__api__autoscaling__v2__CrossVersionObjectReference,
        metric: io__k8s__api__autoscaling__v2__MetricIdentifier,
    ):
        super().__init__()
        if current is not None:
            self._current = current
        if describedObject is not None:
            self._describedObject = describedObject
        if metric is not None:
            self._metric = metric


class io__k8s__api__autoscaling__v2__PodsMetricSource(K8STemplatable):
    """PodsMetricSource indicates how to scale on a metric describing each pod in the current scale target (for example, transactions-processed-per-second). The values will be averaged together before being compared to the target value."""

    props: List[str] = ["metric", "target"]
    required_props: List[str] = ["metric", "target"]

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2__MetricIdentifier:
        return self._metric

    @property
    def target(self) -> io__k8s__api__autoscaling__v2__MetricTarget:
        return self._target

    def __init__(
        self,
        metric: io__k8s__api__autoscaling__v2__MetricIdentifier,
        target: io__k8s__api__autoscaling__v2__MetricTarget,
    ):
        super().__init__()
        if metric is not None:
            self._metric = metric
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2__PodsMetricStatus(K8STemplatable):
    """PodsMetricStatus indicates the current value of a metric describing each pod in the current scale target (for example, transactions-processed-per-second)."""

    props: List[str] = ["current", "metric"]
    required_props: List[str] = ["metric", "current"]

    @property
    def current(self) -> io__k8s__api__autoscaling__v2__MetricValueStatus:
        return self._current

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2__MetricIdentifier:
        return self._metric

    def __init__(
        self,
        current: io__k8s__api__autoscaling__v2__MetricValueStatus,
        metric: io__k8s__api__autoscaling__v2__MetricIdentifier,
    ):
        super().__init__()
        if current is not None:
            self._current = current
        if metric is not None:
            self._metric = metric


class io__k8s__api__autoscaling__v2beta1__ExternalMetricSource(K8STemplatable):
    """ExternalMetricSource indicates how to scale on a metric not associated with any Kubernetes object (for example length of queue in cloud messaging service, or QPS from loadbalancer running outside of cluster). Exactly one "target" type should be set."""

    props: List[str] = [
        "metricName",
        "metricSelector",
        "targetAverageValue",
        "targetValue",
    ]
    required_props: List[str] = ["metricName"]

    @property
    def metricName(self) -> str:
        return self._metricName

    @property
    def metricSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._metricSelector

    @property
    def targetAverageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._targetAverageValue

    @property
    def targetValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._targetValue

    def __init__(
        self,
        metricName: str,
        metricSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        targetAverageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        targetValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
    ):
        super().__init__()
        if metricName is not None:
            self._metricName = metricName
        if metricSelector is not None:
            self._metricSelector = metricSelector
        if targetAverageValue is not None:
            self._targetAverageValue = targetAverageValue
        if targetValue is not None:
            self._targetValue = targetValue


class io__k8s__api__autoscaling__v2beta1__ExternalMetricStatus(K8STemplatable):
    """ExternalMetricStatus indicates the current value of a global metric not associated with any Kubernetes object."""

    props: List[str] = [
        "currentAverageValue",
        "currentValue",
        "metricName",
        "metricSelector",
    ]
    required_props: List[str] = ["metricName", "currentValue"]

    @property
    def currentAverageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._currentAverageValue

    @property
    def currentValue(self) -> io__k8s__apimachinery__pkg__api__resource__Quantity:
        return self._currentValue

    @property
    def metricName(self) -> str:
        return self._metricName

    @property
    def metricSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._metricSelector

    def __init__(
        self,
        currentValue: io__k8s__apimachinery__pkg__api__resource__Quantity,
        metricName: str,
        currentAverageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        metricSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if currentValue is not None:
            self._currentValue = currentValue
        if metricName is not None:
            self._metricName = metricName
        if currentAverageValue is not None:
            self._currentAverageValue = currentAverageValue
        if metricSelector is not None:
            self._metricSelector = metricSelector


class io__k8s__api__autoscaling__v2beta1__ObjectMetricSource(K8STemplatable):
    """ObjectMetricSource indicates how to scale on a metric describing a kubernetes object (for example, hits-per-second on an Ingress object)."""

    props: List[str] = [
        "averageValue",
        "metricName",
        "selector",
        "target",
        "targetValue",
    ]
    required_props: List[str] = ["target", "metricName", "targetValue"]

    @property
    def averageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._averageValue

    @property
    def metricName(self) -> str:
        return self._metricName

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    @property
    def target(self) -> io__k8s__api__autoscaling__v2beta1__CrossVersionObjectReference:
        return self._target

    @property
    def targetValue(self) -> io__k8s__apimachinery__pkg__api__resource__Quantity:
        return self._targetValue

    def __init__(
        self,
        metricName: str,
        target: io__k8s__api__autoscaling__v2beta1__CrossVersionObjectReference,
        targetValue: io__k8s__apimachinery__pkg__api__resource__Quantity,
        averageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if metricName is not None:
            self._metricName = metricName
        if target is not None:
            self._target = target
        if targetValue is not None:
            self._targetValue = targetValue
        if averageValue is not None:
            self._averageValue = averageValue
        if selector is not None:
            self._selector = selector


class io__k8s__api__autoscaling__v2beta1__ObjectMetricStatus(K8STemplatable):
    """ObjectMetricStatus indicates the current value of a metric describing a kubernetes object (for example, hits-per-second on an Ingress object)."""

    props: List[str] = [
        "averageValue",
        "currentValue",
        "metricName",
        "selector",
        "target",
    ]
    required_props: List[str] = ["target", "metricName", "currentValue"]

    @property
    def averageValue(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._averageValue

    @property
    def currentValue(self) -> io__k8s__apimachinery__pkg__api__resource__Quantity:
        return self._currentValue

    @property
    def metricName(self) -> str:
        return self._metricName

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    @property
    def target(self) -> io__k8s__api__autoscaling__v2beta1__CrossVersionObjectReference:
        return self._target

    def __init__(
        self,
        currentValue: io__k8s__apimachinery__pkg__api__resource__Quantity,
        metricName: str,
        target: io__k8s__api__autoscaling__v2beta1__CrossVersionObjectReference,
        averageValue: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if currentValue is not None:
            self._currentValue = currentValue
        if metricName is not None:
            self._metricName = metricName
        if target is not None:
            self._target = target
        if averageValue is not None:
            self._averageValue = averageValue
        if selector is not None:
            self._selector = selector


class io__k8s__api__autoscaling__v2beta1__PodsMetricSource(K8STemplatable):
    """PodsMetricSource indicates how to scale on a metric describing each pod in the current scale target (for example, transactions-processed-per-second). The values will be averaged together before being compared to the target value."""

    props: List[str] = ["metricName", "selector", "targetAverageValue"]
    required_props: List[str] = ["metricName", "targetAverageValue"]

    @property
    def metricName(self) -> str:
        return self._metricName

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    @property
    def targetAverageValue(self) -> io__k8s__apimachinery__pkg__api__resource__Quantity:
        return self._targetAverageValue

    def __init__(
        self,
        metricName: str,
        targetAverageValue: io__k8s__apimachinery__pkg__api__resource__Quantity,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if metricName is not None:
            self._metricName = metricName
        if targetAverageValue is not None:
            self._targetAverageValue = targetAverageValue
        if selector is not None:
            self._selector = selector


class io__k8s__api__autoscaling__v2beta1__PodsMetricStatus(K8STemplatable):
    """PodsMetricStatus indicates the current value of a metric describing each pod in the current scale target (for example, transactions-processed-per-second)."""

    props: List[str] = ["currentAverageValue", "metricName", "selector"]
    required_props: List[str] = ["metricName", "currentAverageValue"]

    @property
    def currentAverageValue(
        self,
    ) -> io__k8s__apimachinery__pkg__api__resource__Quantity:
        return self._currentAverageValue

    @property
    def metricName(self) -> str:
        return self._metricName

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    def __init__(
        self,
        currentAverageValue: io__k8s__apimachinery__pkg__api__resource__Quantity,
        metricName: str,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if currentAverageValue is not None:
            self._currentAverageValue = currentAverageValue
        if metricName is not None:
            self._metricName = metricName
        if selector is not None:
            self._selector = selector


class io__k8s__api__autoscaling__v2beta2__ContainerResourceMetricSource(K8STemplatable):
    """ContainerResourceMetricSource indicates how to scale on a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  The values will be averaged together before being compared to the target.  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.  Only one "target" type should be set."""

    props: List[str] = ["container", "name", "target"]
    required_props: List[str] = ["name", "target", "container"]

    @property
    def container(self) -> str:
        return self._container

    @property
    def name(self) -> str:
        return self._name

    @property
    def target(self) -> io__k8s__api__autoscaling__v2beta2__MetricTarget:
        return self._target

    def __init__(
        self,
        container: str,
        name: str,
        target: io__k8s__api__autoscaling__v2beta2__MetricTarget,
    ):
        super().__init__()
        if container is not None:
            self._container = container
        if name is not None:
            self._name = name
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2beta2__ContainerResourceMetricStatus(K8STemplatable):
    """ContainerResourceMetricStatus indicates the current value of a resource metric known to Kubernetes, as specified in requests and limits, describing a single container in each pod in the current scale target (e.g. CPU or memory).  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source."""

    props: List[str] = ["container", "current", "name"]
    required_props: List[str] = ["name", "current", "container"]

    @property
    def container(self) -> str:
        return self._container

    @property
    def current(self) -> io__k8s__api__autoscaling__v2beta2__MetricValueStatus:
        return self._current

    @property
    def name(self) -> str:
        return self._name

    def __init__(
        self,
        container: str,
        current: io__k8s__api__autoscaling__v2beta2__MetricValueStatus,
        name: str,
    ):
        super().__init__()
        if container is not None:
            self._container = container
        if current is not None:
            self._current = current
        if name is not None:
            self._name = name


class io__k8s__api__autoscaling__v2beta2__MetricIdentifier(K8STemplatable):
    """MetricIdentifier defines the name and optionally selector for a metric"""

    props: List[str] = ["name", "selector"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    def __init__(
        self,
        name: str,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if selector is not None:
            self._selector = selector


class io__k8s__api__autoscaling__v2beta2__ObjectMetricSource(K8STemplatable):
    """ObjectMetricSource indicates how to scale on a metric describing a kubernetes object (for example, hits-per-second on an Ingress object)."""

    props: List[str] = ["describedObject", "metric", "target"]
    required_props: List[str] = ["describedObject", "target", "metric"]

    @property
    def describedObject(
        self,
    ) -> io__k8s__api__autoscaling__v2beta2__CrossVersionObjectReference:
        return self._describedObject

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2beta2__MetricIdentifier:
        return self._metric

    @property
    def target(self) -> io__k8s__api__autoscaling__v2beta2__MetricTarget:
        return self._target

    def __init__(
        self,
        describedObject: io__k8s__api__autoscaling__v2beta2__CrossVersionObjectReference,
        metric: io__k8s__api__autoscaling__v2beta2__MetricIdentifier,
        target: io__k8s__api__autoscaling__v2beta2__MetricTarget,
    ):
        super().__init__()
        if describedObject is not None:
            self._describedObject = describedObject
        if metric is not None:
            self._metric = metric
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2beta2__ObjectMetricStatus(K8STemplatable):
    """ObjectMetricStatus indicates the current value of a metric describing a kubernetes object (for example, hits-per-second on an Ingress object)."""

    props: List[str] = ["current", "describedObject", "metric"]
    required_props: List[str] = ["metric", "current", "describedObject"]

    @property
    def current(self) -> io__k8s__api__autoscaling__v2beta2__MetricValueStatus:
        return self._current

    @property
    def describedObject(
        self,
    ) -> io__k8s__api__autoscaling__v2beta2__CrossVersionObjectReference:
        return self._describedObject

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2beta2__MetricIdentifier:
        return self._metric

    def __init__(
        self,
        current: io__k8s__api__autoscaling__v2beta2__MetricValueStatus,
        describedObject: io__k8s__api__autoscaling__v2beta2__CrossVersionObjectReference,
        metric: io__k8s__api__autoscaling__v2beta2__MetricIdentifier,
    ):
        super().__init__()
        if current is not None:
            self._current = current
        if describedObject is not None:
            self._describedObject = describedObject
        if metric is not None:
            self._metric = metric


class io__k8s__api__autoscaling__v2beta2__PodsMetricSource(K8STemplatable):
    """PodsMetricSource indicates how to scale on a metric describing each pod in the current scale target (for example, transactions-processed-per-second). The values will be averaged together before being compared to the target value."""

    props: List[str] = ["metric", "target"]
    required_props: List[str] = ["metric", "target"]

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2beta2__MetricIdentifier:
        return self._metric

    @property
    def target(self) -> io__k8s__api__autoscaling__v2beta2__MetricTarget:
        return self._target

    def __init__(
        self,
        metric: io__k8s__api__autoscaling__v2beta2__MetricIdentifier,
        target: io__k8s__api__autoscaling__v2beta2__MetricTarget,
    ):
        super().__init__()
        if metric is not None:
            self._metric = metric
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2beta2__PodsMetricStatus(K8STemplatable):
    """PodsMetricStatus indicates the current value of a metric describing each pod in the current scale target (for example, transactions-processed-per-second)."""

    props: List[str] = ["current", "metric"]
    required_props: List[str] = ["metric", "current"]

    @property
    def current(self) -> io__k8s__api__autoscaling__v2beta2__MetricValueStatus:
        return self._current

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2beta2__MetricIdentifier:
        return self._metric

    def __init__(
        self,
        current: io__k8s__api__autoscaling__v2beta2__MetricValueStatus,
        metric: io__k8s__api__autoscaling__v2beta2__MetricIdentifier,
    ):
        super().__init__()
        if current is not None:
            self._current = current
        if metric is not None:
            self._metric = metric


class io__k8s__api__certificates__v1__CertificateSigningRequest(K8STemplatable):
    """CertificateSigningRequest objects provide a mechanism to obtain x509 certificates by submitting a certificate signing request, and having it asynchronously approved and issued.

    Kubelets use this API to obtain:
     1. client certificates to authenticate to kube-apiserver (with the "kubernetes.io/kube-apiserver-client-kubelet" signerName).
     2. serving certificates for TLS endpoints kube-apiserver can connect to securely (with the "kubernetes.io/kubelet-serving" signerName).

    This API can be used to request client certificates to authenticate to kube-apiserver (with the "kubernetes.io/kube-apiserver-client" signerName), or to obtain certificates from custom non-Kubernetes signers."""

    apiVersion: str = "certificates.k8s.io/v1"
    kind: str = "CertificateSigningRequest"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__certificates__v1__CertificateSigningRequestSpec:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__certificates__v1__CertificateSigningRequestStatus]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__certificates__v1__CertificateSigningRequestSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[
            io__k8s__api__certificates__v1__CertificateSigningRequestStatus
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__api__certificates__v1__CertificateSigningRequestList(K8STemplatable):
    """CertificateSigningRequestList is a collection of CertificateSigningRequest objects"""

    apiVersion: str = "certificates.k8s.io/v1"
    kind: str = "CertificateSigningRequestList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__certificates__v1__CertificateSigningRequest]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__certificates__v1__CertificateSigningRequest],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__coordination__v1__Lease(K8STemplatable):
    """Lease defines a lease concept."""

    apiVersion: str = "coordination.k8s.io/v1"
    kind: str = "Lease"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__coordination__v1__LeaseSpec]:
        return self._spec

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__coordination__v1__LeaseSpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec


class io__k8s__api__coordination__v1__LeaseList(K8STemplatable):
    """LeaseList is a list of Lease objects."""

    apiVersion: str = "coordination.k8s.io/v1"
    kind: str = "LeaseList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__coordination__v1__Lease]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__coordination__v1__Lease],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__Binding(K8STemplatable):
    """Binding ties one object to another; for example, a pod is bound to a node by a scheduler. Deprecated in 1.7, please use the bindings subresource of pods instead."""

    apiVersion: str = "v1"
    kind: str = "Binding"

    props: List[str] = ["apiVersion", "kind", "metadata", "target"]
    required_props: List[str] = ["target"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def target(self) -> io__k8s__api__core__v1__ObjectReference:
        return self._target

    def __init__(
        self,
        target: io__k8s__api__core__v1__ObjectReference,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if target is not None:
            self._target = target
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__ComponentStatus(K8STemplatable):
    """ComponentStatus (and ComponentStatusList) holds the cluster validation info. Deprecated: This API is deprecated in v1.19+"""

    apiVersion: str = "v1"
    kind: str = "ComponentStatus"

    props: List[str] = ["apiVersion", "conditions", "kind", "metadata"]
    required_props: List[str] = []

    @property
    def conditions(self) -> Optional[List[io__k8s__api__core__v1__ComponentCondition]]:
        return self._conditions

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    def __init__(
        self,
        conditions: Optional[List[io__k8s__api__core__v1__ComponentCondition]] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__ComponentStatusList(K8STemplatable):
    """Status of all the conditions for the component as a list of ComponentStatus objects. Deprecated: This API is deprecated in v1.19+"""

    apiVersion: str = "v1"
    kind: str = "ComponentStatusList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__ComponentStatus]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__ComponentStatus],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__ConfigMap(K8STemplatable):
    """ConfigMap holds configuration data for pods to consume."""

    apiVersion: str = "v1"
    kind: str = "ConfigMap"

    props: List[str] = [
        "apiVersion",
        "binaryData",
        "data",
        "immutable",
        "kind",
        "metadata",
    ]
    required_props: List[str] = []

    @property
    def binaryData(self) -> Optional[Dict[str, str]]:
        return self._binaryData

    @property
    def data(self) -> Optional[Dict[str, str]]:
        return self._data

    @property
    def immutable(self) -> Optional[bool]:
        return self._immutable

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    def __init__(
        self,
        binaryData: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, str]] = None,
        immutable: Optional[bool] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if binaryData is not None:
            self._binaryData = binaryData
        if data is not None:
            self._data = data
        if immutable is not None:
            self._immutable = immutable
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__ConfigMapList(K8STemplatable):
    """ConfigMapList is a resource containing a list of ConfigMap objects."""

    apiVersion: str = "v1"
    kind: str = "ConfigMapList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__ConfigMap]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__ConfigMap],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__ContainerState(K8STemplatable):
    """ContainerState holds a possible state of container. Only one of its members may be specified. If none of them is specified, the default one is ContainerStateWaiting."""

    props: List[str] = ["running", "terminated", "waiting"]
    required_props: List[str] = []

    @property
    def running(self) -> Optional[io__k8s__api__core__v1__ContainerStateRunning]:
        return self._running

    @property
    def terminated(self) -> Optional[io__k8s__api__core__v1__ContainerStateTerminated]:
        return self._terminated

    @property
    def waiting(self) -> Optional[io__k8s__api__core__v1__ContainerStateWaiting]:
        return self._waiting

    def __init__(
        self,
        running: Optional[io__k8s__api__core__v1__ContainerStateRunning] = None,
        terminated: Optional[io__k8s__api__core__v1__ContainerStateTerminated] = None,
        waiting: Optional[io__k8s__api__core__v1__ContainerStateWaiting] = None,
    ):
        super().__init__()
        if running is not None:
            self._running = running
        if terminated is not None:
            self._terminated = terminated
        if waiting is not None:
            self._waiting = waiting


class io__k8s__api__core__v1__ContainerStatus(K8STemplatable):
    """ContainerStatus contains details for the current status of this container."""

    props: List[str] = [
        "containerID",
        "image",
        "imageID",
        "lastState",
        "name",
        "ready",
        "restartCount",
        "started",
        "state",
    ]
    required_props: List[str] = ["name", "ready", "restartCount", "image", "imageID"]

    @property
    def containerID(self) -> Optional[str]:
        return self._containerID

    @property
    def image(self) -> str:
        return self._image

    @property
    def imageID(self) -> str:
        return self._imageID

    @property
    def lastState(self) -> Optional[io__k8s__api__core__v1__ContainerState]:
        return self._lastState

    @property
    def name(self) -> str:
        return self._name

    @property
    def ready(self) -> bool:
        return self._ready

    @property
    def restartCount(self) -> int:
        return self._restartCount

    @property
    def started(self) -> Optional[bool]:
        return self._started

    @property
    def state(self) -> Optional[io__k8s__api__core__v1__ContainerState]:
        return self._state

    def __init__(
        self,
        image: str,
        imageID: str,
        name: str,
        ready: bool,
        restartCount: int,
        containerID: Optional[str] = None,
        lastState: Optional[io__k8s__api__core__v1__ContainerState] = None,
        started: Optional[bool] = None,
        state: Optional[io__k8s__api__core__v1__ContainerState] = None,
    ):
        super().__init__()
        if image is not None:
            self._image = image
        if imageID is not None:
            self._imageID = imageID
        if name is not None:
            self._name = name
        if ready is not None:
            self._ready = ready
        if restartCount is not None:
            self._restartCount = restartCount
        if containerID is not None:
            self._containerID = containerID
        if lastState is not None:
            self._lastState = lastState
        if started is not None:
            self._started = started
        if state is not None:
            self._state = state


class io__k8s__api__core__v1__DownwardAPIVolumeFile(K8STemplatable):
    """DownwardAPIVolumeFile represents information to create the file containing the pod field"""

    props: List[str] = ["fieldRef", "mode", "path", "resourceFieldRef"]
    required_props: List[str] = ["path"]

    @property
    def fieldRef(self) -> Optional[io__k8s__api__core__v1__ObjectFieldSelector]:
        return self._fieldRef

    @property
    def mode(self) -> Optional[int]:
        return self._mode

    @property
    def path(self) -> str:
        return self._path

    @property
    def resourceFieldRef(
        self,
    ) -> Optional[io__k8s__api__core__v1__ResourceFieldSelector]:
        return self._resourceFieldRef

    def __init__(
        self,
        path: str,
        fieldRef: Optional[io__k8s__api__core__v1__ObjectFieldSelector] = None,
        mode: Optional[int] = None,
        resourceFieldRef: Optional[
            io__k8s__api__core__v1__ResourceFieldSelector
        ] = None,
    ):
        super().__init__()
        if path is not None:
            self._path = path
        if fieldRef is not None:
            self._fieldRef = fieldRef
        if mode is not None:
            self._mode = mode
        if resourceFieldRef is not None:
            self._resourceFieldRef = resourceFieldRef


class io__k8s__api__core__v1__DownwardAPIVolumeSource(K8STemplatable):
    """DownwardAPIVolumeSource represents a volume containing downward API info. Downward API volumes support ownership management and SELinux relabeling."""

    props: List[str] = ["defaultMode", "items"]
    required_props: List[str] = []

    @property
    def defaultMode(self) -> Optional[int]:
        return self._defaultMode

    @property
    def items(self) -> Optional[List[io__k8s__api__core__v1__DownwardAPIVolumeFile]]:
        return self._items

    def __init__(
        self,
        defaultMode: Optional[int] = None,
        items: Optional[List[io__k8s__api__core__v1__DownwardAPIVolumeFile]] = None,
    ):
        super().__init__()
        if defaultMode is not None:
            self._defaultMode = defaultMode
        if items is not None:
            self._items = items


class io__k8s__api__core__v1__Endpoints(K8STemplatable):
    """Endpoints is a collection of endpoints that implement the actual service. Example:
     Name: "mysvc",
     Subsets: [
       {
         Addresses: [{"ip": "10.10.1.1"}, {"ip": "10.10.2.2"}],
         Ports: [{"name": "a", "port": 8675}, {"name": "b", "port": 309}]
       },
       {
         Addresses: [{"ip": "10.10.3.3"}],
         Ports: [{"name": "a", "port": 93}, {"name": "b", "port": 76}]
       },
    ]"""

    apiVersion: str = "v1"
    kind: str = "Endpoints"

    props: List[str] = ["apiVersion", "kind", "metadata", "subsets"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def subsets(self) -> Optional[List[io__k8s__api__core__v1__EndpointSubset]]:
        return self._subsets

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        subsets: Optional[List[io__k8s__api__core__v1__EndpointSubset]] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if subsets is not None:
            self._subsets = subsets


class io__k8s__api__core__v1__EndpointsList(K8STemplatable):
    """EndpointsList is a list of endpoints."""

    apiVersion: str = "v1"
    kind: str = "EndpointsList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__Endpoints]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__Endpoints],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__EnvVarSource(K8STemplatable):
    """EnvVarSource represents a source for the value of an EnvVar."""

    props: List[str] = [
        "configMapKeyRef",
        "fieldRef",
        "resourceFieldRef",
        "secretKeyRef",
    ]
    required_props: List[str] = []

    @property
    def configMapKeyRef(self) -> Optional[io__k8s__api__core__v1__ConfigMapKeySelector]:
        return self._configMapKeyRef

    @property
    def fieldRef(self) -> Optional[io__k8s__api__core__v1__ObjectFieldSelector]:
        return self._fieldRef

    @property
    def resourceFieldRef(
        self,
    ) -> Optional[io__k8s__api__core__v1__ResourceFieldSelector]:
        return self._resourceFieldRef

    @property
    def secretKeyRef(self) -> Optional[io__k8s__api__core__v1__SecretKeySelector]:
        return self._secretKeyRef

    def __init__(
        self,
        configMapKeyRef: Optional[io__k8s__api__core__v1__ConfigMapKeySelector] = None,
        fieldRef: Optional[io__k8s__api__core__v1__ObjectFieldSelector] = None,
        resourceFieldRef: Optional[
            io__k8s__api__core__v1__ResourceFieldSelector
        ] = None,
        secretKeyRef: Optional[io__k8s__api__core__v1__SecretKeySelector] = None,
    ):
        super().__init__()
        if configMapKeyRef is not None:
            self._configMapKeyRef = configMapKeyRef
        if fieldRef is not None:
            self._fieldRef = fieldRef
        if resourceFieldRef is not None:
            self._resourceFieldRef = resourceFieldRef
        if secretKeyRef is not None:
            self._secretKeyRef = secretKeyRef


class io__k8s__api__core__v1__Event(K8STemplatable):
    """Event is a report of an event somewhere in the cluster.  Events have a limited retention time and triggers and messages may evolve with time.  Event consumers should not rely on the timing of an event with a given Reason reflecting a consistent underlying trigger, or the continued existence of events with that Reason.  Events should be treated as informative, best-effort, supplemental data."""

    apiVersion: str = "v1"
    kind: str = "Event"

    props: List[str] = [
        "action",
        "apiVersion",
        "count",
        "eventTime",
        "firstTimestamp",
        "involvedObject",
        "kind",
        "lastTimestamp",
        "message",
        "metadata",
        "reason",
        "related",
        "reportingComponent",
        "reportingInstance",
        "series",
        "source",
        "type",
    ]
    required_props: List[str] = ["metadata", "involvedObject"]

    @property
    def action(self) -> Optional[str]:
        return self._action

    @property
    def count(self) -> Optional[int]:
        return self._count

    @property
    def eventTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime]:
        return self._eventTime

    @property
    def firstTimestamp(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._firstTimestamp

    @property
    def involvedObject(self) -> io__k8s__api__core__v1__ObjectReference:
        return self._involvedObject

    @property
    def lastTimestamp(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastTimestamp

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def metadata(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta:
        return self._metadata

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def related(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._related

    @property
    def reportingComponent(self) -> Optional[str]:
        return self._reportingComponent

    @property
    def reportingInstance(self) -> Optional[str]:
        return self._reportingInstance

    @property
    def series(self) -> Optional[io__k8s__api__core__v1__EventSeries]:
        return self._series

    @property
    def source(self) -> Optional[io__k8s__api__core__v1__EventSource]:
        return self._source

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(
        self,
        involvedObject: io__k8s__api__core__v1__ObjectReference,
        metadata: io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta,
        action: Optional[str] = None,
        count: Optional[int] = None,
        eventTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime
        ] = None,
        firstTimestamp: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        lastTimestamp: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
        related: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        reportingComponent: Optional[str] = None,
        reportingInstance: Optional[str] = None,
        series: Optional[io__k8s__api__core__v1__EventSeries] = None,
        source: Optional[io__k8s__api__core__v1__EventSource] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        if involvedObject is not None:
            self._involvedObject = involvedObject
        if metadata is not None:
            self._metadata = metadata
        if action is not None:
            self._action = action
        if count is not None:
            self._count = count
        if eventTime is not None:
            self._eventTime = eventTime
        if firstTimestamp is not None:
            self._firstTimestamp = firstTimestamp
        if lastTimestamp is not None:
            self._lastTimestamp = lastTimestamp
        if message is not None:
            self._message = message
        if reason is not None:
            self._reason = reason
        if related is not None:
            self._related = related
        if reportingComponent is not None:
            self._reportingComponent = reportingComponent
        if reportingInstance is not None:
            self._reportingInstance = reportingInstance
        if series is not None:
            self._series = series
        if source is not None:
            self._source = source
        if type is not None:
            self._type = type


class io__k8s__api__core__v1__EventList(K8STemplatable):
    """EventList is a list of events."""

    apiVersion: str = "v1"
    kind: str = "EventList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__Event]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__Event],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__LifecycleHandler(K8STemplatable):
    """LifecycleHandler defines a specific action that should be taken in a lifecycle hook. One and only one of the fields, except TCPSocket must be specified."""

    props: List[str] = ["exec", "httpGet", "tcpSocket"]
    required_props: List[str] = []

    @property
    def exec(self) -> Optional[io__k8s__api__core__v1__ExecAction]:
        return self._exec

    @property
    def httpGet(self) -> Optional[io__k8s__api__core__v1__HTTPGetAction]:
        return self._httpGet

    @property
    def tcpSocket(self) -> Optional[io__k8s__api__core__v1__TCPSocketAction]:
        return self._tcpSocket

    def __init__(
        self,
        exec: Optional[io__k8s__api__core__v1__ExecAction] = None,
        httpGet: Optional[io__k8s__api__core__v1__HTTPGetAction] = None,
        tcpSocket: Optional[io__k8s__api__core__v1__TCPSocketAction] = None,
    ):
        super().__init__()
        if exec is not None:
            self._exec = exec
        if httpGet is not None:
            self._httpGet = httpGet
        if tcpSocket is not None:
            self._tcpSocket = tcpSocket


class io__k8s__api__core__v1__LimitRange(K8STemplatable):
    """LimitRange sets resource usage limits for each kind of resource in a Namespace."""

    apiVersion: str = "v1"
    kind: str = "LimitRange"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__LimitRangeSpec]:
        return self._spec

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__LimitRangeSpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec


class io__k8s__api__core__v1__LimitRangeList(K8STemplatable):
    """LimitRangeList is a list of LimitRange items."""

    apiVersion: str = "v1"
    kind: str = "LimitRangeList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__LimitRange]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__LimitRange],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__Namespace(K8STemplatable):
    """Namespace provides a scope for Names. Use of multiple namespaces is optional."""

    apiVersion: str = "v1"
    kind: str = "Namespace"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__NamespaceSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__core__v1__NamespaceStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__NamespaceSpec] = None,
        status: Optional[io__k8s__api__core__v1__NamespaceStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__core__v1__NamespaceList(K8STemplatable):
    """NamespaceList is a list of Namespaces."""

    apiVersion: str = "v1"
    kind: str = "NamespaceList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__Namespace]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__Namespace],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__NodeAffinity(K8STemplatable):
    """Node affinity is a group of node affinity scheduling rules."""

    props: List[str] = [
        "preferredDuringSchedulingIgnoredDuringExecution",
        "requiredDuringSchedulingIgnoredDuringExecution",
    ]
    required_props: List[str] = []

    @property
    def preferredDuringSchedulingIgnoredDuringExecution(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__PreferredSchedulingTerm]]:
        return self._preferredDuringSchedulingIgnoredDuringExecution

    @property
    def requiredDuringSchedulingIgnoredDuringExecution(
        self,
    ) -> Optional[io__k8s__api__core__v1__NodeSelector]:
        return self._requiredDuringSchedulingIgnoredDuringExecution

    def __init__(
        self,
        preferredDuringSchedulingIgnoredDuringExecution: Optional[
            List[io__k8s__api__core__v1__PreferredSchedulingTerm]
        ] = None,
        requiredDuringSchedulingIgnoredDuringExecution: Optional[
            io__k8s__api__core__v1__NodeSelector
        ] = None,
    ):
        super().__init__()
        if preferredDuringSchedulingIgnoredDuringExecution is not None:
            self._preferredDuringSchedulingIgnoredDuringExecution = (
                preferredDuringSchedulingIgnoredDuringExecution
            )
        if requiredDuringSchedulingIgnoredDuringExecution is not None:
            self._requiredDuringSchedulingIgnoredDuringExecution = (
                requiredDuringSchedulingIgnoredDuringExecution
            )


class io__k8s__api__core__v1__NodeSpec(K8STemplatable):
    """NodeSpec describes the attributes that a node is created with."""

    props: List[str] = [
        "configSource",
        "externalID",
        "podCIDR",
        "podCIDRs",
        "providerID",
        "taints",
        "unschedulable",
    ]
    required_props: List[str] = []

    @property
    def configSource(self) -> Optional[io__k8s__api__core__v1__NodeConfigSource]:
        return self._configSource

    @property
    def externalID(self) -> Optional[str]:
        return self._externalID

    @property
    def podCIDR(self) -> Optional[str]:
        return self._podCIDR

    @property
    def podCIDRs(self) -> Optional[List[str]]:
        return self._podCIDRs

    @property
    def providerID(self) -> Optional[str]:
        return self._providerID

    @property
    def taints(self) -> Optional[List[io__k8s__api__core__v1__Taint]]:
        return self._taints

    @property
    def unschedulable(self) -> Optional[bool]:
        return self._unschedulable

    def __init__(
        self,
        configSource: Optional[io__k8s__api__core__v1__NodeConfigSource] = None,
        externalID: Optional[str] = None,
        podCIDR: Optional[str] = None,
        podCIDRs: Optional[List[str]] = None,
        providerID: Optional[str] = None,
        taints: Optional[List[io__k8s__api__core__v1__Taint]] = None,
        unschedulable: Optional[bool] = None,
    ):
        super().__init__()
        if configSource is not None:
            self._configSource = configSource
        if externalID is not None:
            self._externalID = externalID
        if podCIDR is not None:
            self._podCIDR = podCIDR
        if podCIDRs is not None:
            self._podCIDRs = podCIDRs
        if providerID is not None:
            self._providerID = providerID
        if taints is not None:
            self._taints = taints
        if unschedulable is not None:
            self._unschedulable = unschedulable


class io__k8s__api__core__v1__PersistentVolumeClaimSpec(K8STemplatable):
    """PersistentVolumeClaimSpec describes the common attributes of storage devices and allows a Source for provider-specific attributes"""

    props: List[str] = [
        "accessModes",
        "dataSource",
        "dataSourceRef",
        "resources",
        "selector",
        "storageClassName",
        "volumeMode",
        "volumeName",
    ]
    required_props: List[str] = []

    @property
    def accessModes(self) -> Optional[List[str]]:
        return self._accessModes

    @property
    def dataSource(self) -> Optional[io__k8s__api__core__v1__TypedLocalObjectReference]:
        return self._dataSource

    @property
    def dataSourceRef(
        self,
    ) -> Optional[io__k8s__api__core__v1__TypedLocalObjectReference]:
        return self._dataSourceRef

    @property
    def resources(self) -> Optional[io__k8s__api__core__v1__ResourceRequirements]:
        return self._resources

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    @property
    def storageClassName(self) -> Optional[str]:
        return self._storageClassName

    @property
    def volumeMode(self) -> Optional[str]:
        return self._volumeMode

    @property
    def volumeName(self) -> Optional[str]:
        return self._volumeName

    def __init__(
        self,
        accessModes: Optional[List[str]] = None,
        dataSource: Optional[io__k8s__api__core__v1__TypedLocalObjectReference] = None,
        dataSourceRef: Optional[
            io__k8s__api__core__v1__TypedLocalObjectReference
        ] = None,
        resources: Optional[io__k8s__api__core__v1__ResourceRequirements] = None,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        storageClassName: Optional[str] = None,
        volumeMode: Optional[str] = None,
        volumeName: Optional[str] = None,
    ):
        super().__init__()
        if accessModes is not None:
            self._accessModes = accessModes
        if dataSource is not None:
            self._dataSource = dataSource
        if dataSourceRef is not None:
            self._dataSourceRef = dataSourceRef
        if resources is not None:
            self._resources = resources
        if selector is not None:
            self._selector = selector
        if storageClassName is not None:
            self._storageClassName = storageClassName
        if volumeMode is not None:
            self._volumeMode = volumeMode
        if volumeName is not None:
            self._volumeName = volumeName


class io__k8s__api__core__v1__PersistentVolumeClaimTemplate(K8STemplatable):
    """PersistentVolumeClaimTemplate is used to produce PersistentVolumeClaim objects as part of an EphemeralVolumeSource."""

    props: List[str] = ["metadata", "spec"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__core__v1__PersistentVolumeClaimSpec:
        return self._spec

    def __init__(
        self,
        spec: io__k8s__api__core__v1__PersistentVolumeClaimSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__PersistentVolumeSpec(K8STemplatable):
    """PersistentVolumeSpec is the specification of a persistent volume."""

    props: List[str] = [
        "accessModes",
        "awsElasticBlockStore",
        "azureDisk",
        "azureFile",
        "capacity",
        "cephfs",
        "cinder",
        "claimRef",
        "csi",
        "fc",
        "flexVolume",
        "flocker",
        "gcePersistentDisk",
        "glusterfs",
        "hostPath",
        "iscsi",
        "local",
        "mountOptions",
        "nfs",
        "nodeAffinity",
        "persistentVolumeReclaimPolicy",
        "photonPersistentDisk",
        "portworxVolume",
        "quobyte",
        "rbd",
        "scaleIO",
        "storageClassName",
        "storageos",
        "volumeMode",
        "vsphereVolume",
    ]
    required_props: List[str] = []

    @property
    def accessModes(self) -> Optional[List[str]]:
        return self._accessModes

    @property
    def awsElasticBlockStore(
        self,
    ) -> Optional[io__k8s__api__core__v1__AWSElasticBlockStoreVolumeSource]:
        return self._awsElasticBlockStore

    @property
    def azureDisk(self) -> Optional[io__k8s__api__core__v1__AzureDiskVolumeSource]:
        return self._azureDisk

    @property
    def azureFile(
        self,
    ) -> Optional[io__k8s__api__core__v1__AzureFilePersistentVolumeSource]:
        return self._azureFile

    @property
    def capacity(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._capacity

    @property
    def cephfs(self) -> Optional[io__k8s__api__core__v1__CephFSPersistentVolumeSource]:
        return self._cephfs

    @property
    def cinder(self) -> Optional[io__k8s__api__core__v1__CinderPersistentVolumeSource]:
        return self._cinder

    @property
    def claimRef(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._claimRef

    @property
    def csi(self) -> Optional[io__k8s__api__core__v1__CSIPersistentVolumeSource]:
        return self._csi

    @property
    def fc(self) -> Optional[io__k8s__api__core__v1__FCVolumeSource]:
        return self._fc

    @property
    def flexVolume(
        self,
    ) -> Optional[io__k8s__api__core__v1__FlexPersistentVolumeSource]:
        return self._flexVolume

    @property
    def flocker(self) -> Optional[io__k8s__api__core__v1__FlockerVolumeSource]:
        return self._flocker

    @property
    def gcePersistentDisk(
        self,
    ) -> Optional[io__k8s__api__core__v1__GCEPersistentDiskVolumeSource]:
        return self._gcePersistentDisk

    @property
    def glusterfs(
        self,
    ) -> Optional[io__k8s__api__core__v1__GlusterfsPersistentVolumeSource]:
        return self._glusterfs

    @property
    def hostPath(self) -> Optional[io__k8s__api__core__v1__HostPathVolumeSource]:
        return self._hostPath

    @property
    def iscsi(self) -> Optional[io__k8s__api__core__v1__ISCSIPersistentVolumeSource]:
        return self._iscsi

    @property
    def local(self) -> Optional[io__k8s__api__core__v1__LocalVolumeSource]:
        return self._local

    @property
    def mountOptions(self) -> Optional[List[str]]:
        return self._mountOptions

    @property
    def nfs(self) -> Optional[io__k8s__api__core__v1__NFSVolumeSource]:
        return self._nfs

    @property
    def nodeAffinity(self) -> Optional[io__k8s__api__core__v1__VolumeNodeAffinity]:
        return self._nodeAffinity

    @property
    def persistentVolumeReclaimPolicy(
        self,
    ) -> Optional[Literal["Delete", "Recycle", "Retain"]]:
        return self._persistentVolumeReclaimPolicy

    @property
    def photonPersistentDisk(
        self,
    ) -> Optional[io__k8s__api__core__v1__PhotonPersistentDiskVolumeSource]:
        return self._photonPersistentDisk

    @property
    def portworxVolume(self) -> Optional[io__k8s__api__core__v1__PortworxVolumeSource]:
        return self._portworxVolume

    @property
    def quobyte(self) -> Optional[io__k8s__api__core__v1__QuobyteVolumeSource]:
        return self._quobyte

    @property
    def rbd(self) -> Optional[io__k8s__api__core__v1__RBDPersistentVolumeSource]:
        return self._rbd

    @property
    def scaleIO(
        self,
    ) -> Optional[io__k8s__api__core__v1__ScaleIOPersistentVolumeSource]:
        return self._scaleIO

    @property
    def storageClassName(self) -> Optional[str]:
        return self._storageClassName

    @property
    def storageos(
        self,
    ) -> Optional[io__k8s__api__core__v1__StorageOSPersistentVolumeSource]:
        return self._storageos

    @property
    def volumeMode(self) -> Optional[str]:
        return self._volumeMode

    @property
    def vsphereVolume(
        self,
    ) -> Optional[io__k8s__api__core__v1__VsphereVirtualDiskVolumeSource]:
        return self._vsphereVolume

    def __init__(
        self,
        accessModes: Optional[List[str]] = None,
        awsElasticBlockStore: Optional[
            io__k8s__api__core__v1__AWSElasticBlockStoreVolumeSource
        ] = None,
        azureDisk: Optional[io__k8s__api__core__v1__AzureDiskVolumeSource] = None,
        azureFile: Optional[
            io__k8s__api__core__v1__AzureFilePersistentVolumeSource
        ] = None,
        capacity: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        cephfs: Optional[io__k8s__api__core__v1__CephFSPersistentVolumeSource] = None,
        cinder: Optional[io__k8s__api__core__v1__CinderPersistentVolumeSource] = None,
        claimRef: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        csi: Optional[io__k8s__api__core__v1__CSIPersistentVolumeSource] = None,
        fc: Optional[io__k8s__api__core__v1__FCVolumeSource] = None,
        flexVolume: Optional[io__k8s__api__core__v1__FlexPersistentVolumeSource] = None,
        flocker: Optional[io__k8s__api__core__v1__FlockerVolumeSource] = None,
        gcePersistentDisk: Optional[
            io__k8s__api__core__v1__GCEPersistentDiskVolumeSource
        ] = None,
        glusterfs: Optional[
            io__k8s__api__core__v1__GlusterfsPersistentVolumeSource
        ] = None,
        hostPath: Optional[io__k8s__api__core__v1__HostPathVolumeSource] = None,
        iscsi: Optional[io__k8s__api__core__v1__ISCSIPersistentVolumeSource] = None,
        local: Optional[io__k8s__api__core__v1__LocalVolumeSource] = None,
        mountOptions: Optional[List[str]] = None,
        nfs: Optional[io__k8s__api__core__v1__NFSVolumeSource] = None,
        nodeAffinity: Optional[io__k8s__api__core__v1__VolumeNodeAffinity] = None,
        persistentVolumeReclaimPolicy: Optional[
            Literal["Delete", "Recycle", "Retain"]
        ] = None,
        photonPersistentDisk: Optional[
            io__k8s__api__core__v1__PhotonPersistentDiskVolumeSource
        ] = None,
        portworxVolume: Optional[io__k8s__api__core__v1__PortworxVolumeSource] = None,
        quobyte: Optional[io__k8s__api__core__v1__QuobyteVolumeSource] = None,
        rbd: Optional[io__k8s__api__core__v1__RBDPersistentVolumeSource] = None,
        scaleIO: Optional[io__k8s__api__core__v1__ScaleIOPersistentVolumeSource] = None,
        storageClassName: Optional[str] = None,
        storageos: Optional[
            io__k8s__api__core__v1__StorageOSPersistentVolumeSource
        ] = None,
        volumeMode: Optional[str] = None,
        vsphereVolume: Optional[
            io__k8s__api__core__v1__VsphereVirtualDiskVolumeSource
        ] = None,
    ):
        super().__init__()
        if accessModes is not None:
            self._accessModes = accessModes
        if awsElasticBlockStore is not None:
            self._awsElasticBlockStore = awsElasticBlockStore
        if azureDisk is not None:
            self._azureDisk = azureDisk
        if azureFile is not None:
            self._azureFile = azureFile
        if capacity is not None:
            self._capacity = capacity
        if cephfs is not None:
            self._cephfs = cephfs
        if cinder is not None:
            self._cinder = cinder
        if claimRef is not None:
            self._claimRef = claimRef
        if csi is not None:
            self._csi = csi
        if fc is not None:
            self._fc = fc
        if flexVolume is not None:
            self._flexVolume = flexVolume
        if flocker is not None:
            self._flocker = flocker
        if gcePersistentDisk is not None:
            self._gcePersistentDisk = gcePersistentDisk
        if glusterfs is not None:
            self._glusterfs = glusterfs
        if hostPath is not None:
            self._hostPath = hostPath
        if iscsi is not None:
            self._iscsi = iscsi
        if local is not None:
            self._local = local
        if mountOptions is not None:
            self._mountOptions = mountOptions
        if nfs is not None:
            self._nfs = nfs
        if nodeAffinity is not None:
            self._nodeAffinity = nodeAffinity
        if persistentVolumeReclaimPolicy is not None:
            self._persistentVolumeReclaimPolicy = persistentVolumeReclaimPolicy
        if photonPersistentDisk is not None:
            self._photonPersistentDisk = photonPersistentDisk
        if portworxVolume is not None:
            self._portworxVolume = portworxVolume
        if quobyte is not None:
            self._quobyte = quobyte
        if rbd is not None:
            self._rbd = rbd
        if scaleIO is not None:
            self._scaleIO = scaleIO
        if storageClassName is not None:
            self._storageClassName = storageClassName
        if storageos is not None:
            self._storageos = storageos
        if volumeMode is not None:
            self._volumeMode = volumeMode
        if vsphereVolume is not None:
            self._vsphereVolume = vsphereVolume


class io__k8s__api__core__v1__PodAffinityTerm(K8STemplatable):
    """Defines a set of pods (namely those matching the labelSelector relative to the given namespace(s)) that this pod should be co-located (affinity) or not co-located (anti-affinity) with, where co-located is defined as running on a node whose value of the label with key <topologyKey> matches that of any node on which a pod of the set of pods is running"""

    props: List[str] = [
        "labelSelector",
        "namespaceSelector",
        "namespaces",
        "topologyKey",
    ]
    required_props: List[str] = ["topologyKey"]

    @property
    def labelSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._labelSelector

    @property
    def namespaceSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._namespaceSelector

    @property
    def namespaces(self) -> Optional[List[str]]:
        return self._namespaces

    @property
    def topologyKey(self) -> str:
        return self._topologyKey

    def __init__(
        self,
        topologyKey: str,
        labelSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        namespaceSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        namespaces: Optional[List[str]] = None,
    ):
        super().__init__()
        if topologyKey is not None:
            self._topologyKey = topologyKey
        if labelSelector is not None:
            self._labelSelector = labelSelector
        if namespaceSelector is not None:
            self._namespaceSelector = namespaceSelector
        if namespaces is not None:
            self._namespaces = namespaces


class io__k8s__api__core__v1__PodStatus(K8STemplatable):
    """PodStatus represents information about the status of a pod. Status may trail the actual state of a system, especially if the node that hosts the pod cannot contact the control plane."""

    props: List[str] = [
        "conditions",
        "containerStatuses",
        "ephemeralContainerStatuses",
        "hostIP",
        "initContainerStatuses",
        "message",
        "nominatedNodeName",
        "phase",
        "podIP",
        "podIPs",
        "qosClass",
        "reason",
        "startTime",
    ]
    required_props: List[str] = []

    @property
    def conditions(self) -> Optional[List[io__k8s__api__core__v1__PodCondition]]:
        return self._conditions

    @property
    def containerStatuses(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__ContainerStatus]]:
        return self._containerStatuses

    @property
    def ephemeralContainerStatuses(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__ContainerStatus]]:
        return self._ephemeralContainerStatuses

    @property
    def hostIP(self) -> Optional[str]:
        return self._hostIP

    @property
    def initContainerStatuses(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__ContainerStatus]]:
        return self._initContainerStatuses

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def nominatedNodeName(self) -> Optional[str]:
        return self._nominatedNodeName

    @property
    def phase(
        self,
    ) -> Optional[Literal["Failed", "Pending", "Running", "Succeeded", "Unknown"]]:
        return self._phase

    @property
    def podIP(self) -> Optional[str]:
        return self._podIP

    @property
    def podIPs(self) -> Optional[List[io__k8s__api__core__v1__PodIP]]:
        return self._podIPs

    @property
    def qosClass(self) -> Optional[Literal["BestEffort", "Burstable", "Guaranteed"]]:
        return self._qosClass

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def startTime(self) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._startTime

    def __init__(
        self,
        conditions: Optional[List[io__k8s__api__core__v1__PodCondition]] = None,
        containerStatuses: Optional[
            List[io__k8s__api__core__v1__ContainerStatus]
        ] = None,
        ephemeralContainerStatuses: Optional[
            List[io__k8s__api__core__v1__ContainerStatus]
        ] = None,
        hostIP: Optional[str] = None,
        initContainerStatuses: Optional[
            List[io__k8s__api__core__v1__ContainerStatus]
        ] = None,
        message: Optional[str] = None,
        nominatedNodeName: Optional[str] = None,
        phase: Optional[
            Literal["Failed", "Pending", "Running", "Succeeded", "Unknown"]
        ] = None,
        podIP: Optional[str] = None,
        podIPs: Optional[List[io__k8s__api__core__v1__PodIP]] = None,
        qosClass: Optional[Literal["BestEffort", "Burstable", "Guaranteed"]] = None,
        reason: Optional[str] = None,
        startTime: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions
        if containerStatuses is not None:
            self._containerStatuses = containerStatuses
        if ephemeralContainerStatuses is not None:
            self._ephemeralContainerStatuses = ephemeralContainerStatuses
        if hostIP is not None:
            self._hostIP = hostIP
        if initContainerStatuses is not None:
            self._initContainerStatuses = initContainerStatuses
        if message is not None:
            self._message = message
        if nominatedNodeName is not None:
            self._nominatedNodeName = nominatedNodeName
        if phase is not None:
            self._phase = phase
        if podIP is not None:
            self._podIP = podIP
        if podIPs is not None:
            self._podIPs = podIPs
        if qosClass is not None:
            self._qosClass = qosClass
        if reason is not None:
            self._reason = reason
        if startTime is not None:
            self._startTime = startTime


class io__k8s__api__core__v1__Probe(K8STemplatable):
    """Probe describes a health check to be performed against a container to determine whether it is alive or ready to receive traffic."""

    props: List[str] = [
        "exec",
        "failureThreshold",
        "grpc",
        "httpGet",
        "initialDelaySeconds",
        "periodSeconds",
        "successThreshold",
        "tcpSocket",
        "terminationGracePeriodSeconds",
        "timeoutSeconds",
    ]
    required_props: List[str] = []

    @property
    def exec(self) -> Optional[io__k8s__api__core__v1__ExecAction]:
        return self._exec

    @property
    def failureThreshold(self) -> Optional[int]:
        return self._failureThreshold

    @property
    def grpc(self) -> Optional[io__k8s__api__core__v1__GRPCAction]:
        return self._grpc

    @property
    def httpGet(self) -> Optional[io__k8s__api__core__v1__HTTPGetAction]:
        return self._httpGet

    @property
    def initialDelaySeconds(self) -> Optional[int]:
        return self._initialDelaySeconds

    @property
    def periodSeconds(self) -> Optional[int]:
        return self._periodSeconds

    @property
    def successThreshold(self) -> Optional[int]:
        return self._successThreshold

    @property
    def tcpSocket(self) -> Optional[io__k8s__api__core__v1__TCPSocketAction]:
        return self._tcpSocket

    @property
    def terminationGracePeriodSeconds(self) -> Optional[int]:
        return self._terminationGracePeriodSeconds

    @property
    def timeoutSeconds(self) -> Optional[int]:
        return self._timeoutSeconds

    def __init__(
        self,
        exec: Optional[io__k8s__api__core__v1__ExecAction] = None,
        failureThreshold: Optional[int] = None,
        grpc: Optional[io__k8s__api__core__v1__GRPCAction] = None,
        httpGet: Optional[io__k8s__api__core__v1__HTTPGetAction] = None,
        initialDelaySeconds: Optional[int] = None,
        periodSeconds: Optional[int] = None,
        successThreshold: Optional[int] = None,
        tcpSocket: Optional[io__k8s__api__core__v1__TCPSocketAction] = None,
        terminationGracePeriodSeconds: Optional[int] = None,
        timeoutSeconds: Optional[int] = None,
    ):
        super().__init__()
        if exec is not None:
            self._exec = exec
        if failureThreshold is not None:
            self._failureThreshold = failureThreshold
        if grpc is not None:
            self._grpc = grpc
        if httpGet is not None:
            self._httpGet = httpGet
        if initialDelaySeconds is not None:
            self._initialDelaySeconds = initialDelaySeconds
        if periodSeconds is not None:
            self._periodSeconds = periodSeconds
        if successThreshold is not None:
            self._successThreshold = successThreshold
        if tcpSocket is not None:
            self._tcpSocket = tcpSocket
        if terminationGracePeriodSeconds is not None:
            self._terminationGracePeriodSeconds = terminationGracePeriodSeconds
        if timeoutSeconds is not None:
            self._timeoutSeconds = timeoutSeconds


class io__k8s__api__core__v1__ResourceQuotaSpec(K8STemplatable):
    """ResourceQuotaSpec defines the desired hard limits to enforce for Quota."""

    props: List[str] = ["hard", "scopeSelector", "scopes"]
    required_props: List[str] = []

    @property
    def hard(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._hard

    @property
    def scopeSelector(self) -> Optional[io__k8s__api__core__v1__ScopeSelector]:
        return self._scopeSelector

    @property
    def scopes(self) -> Optional[List[str]]:
        return self._scopes

    def __init__(
        self,
        hard: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        scopeSelector: Optional[io__k8s__api__core__v1__ScopeSelector] = None,
        scopes: Optional[List[str]] = None,
    ):
        super().__init__()
        if hard is not None:
            self._hard = hard
        if scopeSelector is not None:
            self._scopeSelector = scopeSelector
        if scopes is not None:
            self._scopes = scopes


class io__k8s__api__core__v1__Secret(K8STemplatable):
    """Secret holds secret data of a certain type. The total bytes of the values in the Data field must be less than MaxSecretSize bytes."""

    apiVersion: str = "v1"
    kind: str = "Secret"

    props: List[str] = [
        "apiVersion",
        "data",
        "immutable",
        "kind",
        "metadata",
        "stringData",
        "type",
    ]
    required_props: List[str] = []

    @property
    def data(self) -> Optional[Dict[str, str]]:
        return self._data

    @property
    def immutable(self) -> Optional[bool]:
        return self._immutable

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def stringData(self) -> Optional[Dict[str, str]]:
        return self._stringData

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(
        self,
        data: Optional[Dict[str, str]] = None,
        immutable: Optional[bool] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        stringData: Optional[Dict[str, str]] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        if data is not None:
            self._data = data
        if immutable is not None:
            self._immutable = immutable
        if metadata is not None:
            self._metadata = metadata
        if stringData is not None:
            self._stringData = stringData
        if type is not None:
            self._type = type


class io__k8s__api__core__v1__SecretList(K8STemplatable):
    """SecretList is a list of Secret."""

    apiVersion: str = "v1"
    kind: str = "SecretList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__Secret]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__Secret],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__ServiceAccount(K8STemplatable):
    """ServiceAccount binds together: * a name, understood by users, and perhaps by peripheral systems, for an identity * a principal that can be authenticated and authorized * a set of secrets"""

    apiVersion: str = "v1"
    kind: str = "ServiceAccount"

    props: List[str] = [
        "apiVersion",
        "automountServiceAccountToken",
        "imagePullSecrets",
        "kind",
        "metadata",
        "secrets",
    ]
    required_props: List[str] = []

    @property
    def automountServiceAccountToken(self) -> Optional[bool]:
        return self._automountServiceAccountToken

    @property
    def imagePullSecrets(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__LocalObjectReference]]:
        return self._imagePullSecrets

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def secrets(self) -> Optional[List[io__k8s__api__core__v1__ObjectReference]]:
        return self._secrets

    def __init__(
        self,
        automountServiceAccountToken: Optional[bool] = None,
        imagePullSecrets: Optional[
            List[io__k8s__api__core__v1__LocalObjectReference]
        ] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        secrets: Optional[List[io__k8s__api__core__v1__ObjectReference]] = None,
    ):
        super().__init__()
        if automountServiceAccountToken is not None:
            self._automountServiceAccountToken = automountServiceAccountToken
        if imagePullSecrets is not None:
            self._imagePullSecrets = imagePullSecrets
        if metadata is not None:
            self._metadata = metadata
        if secrets is not None:
            self._secrets = secrets


class io__k8s__api__core__v1__ServiceAccountList(K8STemplatable):
    """ServiceAccountList is a list of ServiceAccount objects"""

    apiVersion: str = "v1"
    kind: str = "ServiceAccountList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__ServiceAccount]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__ServiceAccount],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__ServiceStatus(K8STemplatable):
    """ServiceStatus represents the current status of a service."""

    props: List[str] = ["conditions", "loadBalancer"]
    required_props: List[str] = []

    @property
    def conditions(
        self,
    ) -> Optional[List[io__k8s__apimachinery__pkg__apis__meta__v1__Condition]]:
        return self._conditions

    @property
    def loadBalancer(self) -> Optional[io__k8s__api__core__v1__LoadBalancerStatus]:
        return self._loadBalancer

    def __init__(
        self,
        conditions: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__Condition]
        ] = None,
        loadBalancer: Optional[io__k8s__api__core__v1__LoadBalancerStatus] = None,
    ):
        super().__init__()
        if conditions is not None:
            self._conditions = conditions
        if loadBalancer is not None:
            self._loadBalancer = loadBalancer


class io__k8s__api__core__v1__TopologySpreadConstraint(K8STemplatable):
    """TopologySpreadConstraint specifies how to spread matching pods among the given topology."""

    props: List[str] = [
        "labelSelector",
        "maxSkew",
        "minDomains",
        "topologyKey",
        "whenUnsatisfiable",
    ]
    required_props: List[str] = ["maxSkew", "topologyKey", "whenUnsatisfiable"]

    @property
    def labelSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._labelSelector

    @property
    def maxSkew(self) -> int:
        return self._maxSkew

    @property
    def minDomains(self) -> Optional[int]:
        return self._minDomains

    @property
    def topologyKey(self) -> str:
        return self._topologyKey

    @property
    def whenUnsatisfiable(self) -> Literal["DoNotSchedule", "ScheduleAnyway"]:
        return self._whenUnsatisfiable

    def __init__(
        self,
        maxSkew: int,
        topologyKey: str,
        whenUnsatisfiable: Literal["DoNotSchedule", "ScheduleAnyway"],
        labelSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        minDomains: Optional[int] = None,
    ):
        super().__init__()
        if maxSkew is not None:
            self._maxSkew = maxSkew
        if topologyKey is not None:
            self._topologyKey = topologyKey
        if whenUnsatisfiable is not None:
            self._whenUnsatisfiable = whenUnsatisfiable
        if labelSelector is not None:
            self._labelSelector = labelSelector
        if minDomains is not None:
            self._minDomains = minDomains


class io__k8s__api__core__v1__WeightedPodAffinityTerm(K8STemplatable):
    """The weights of all of the matched WeightedPodAffinityTerm fields are added per-node to find the most preferred node(s)"""

    props: List[str] = ["podAffinityTerm", "weight"]
    required_props: List[str] = ["weight", "podAffinityTerm"]

    @property
    def podAffinityTerm(self) -> io__k8s__api__core__v1__PodAffinityTerm:
        return self._podAffinityTerm

    @property
    def weight(self) -> int:
        return self._weight

    def __init__(
        self, podAffinityTerm: io__k8s__api__core__v1__PodAffinityTerm, weight: int
    ):
        super().__init__()
        if podAffinityTerm is not None:
            self._podAffinityTerm = podAffinityTerm
        if weight is not None:
            self._weight = weight


class io__k8s__api__discovery__v1__Endpoint(K8STemplatable):
    """Endpoint represents a single logical "backend" implementing a service."""

    props: List[str] = [
        "addresses",
        "conditions",
        "deprecatedTopology",
        "hints",
        "hostname",
        "nodeName",
        "targetRef",
        "zone",
    ]
    required_props: List[str] = ["addresses"]

    @property
    def addresses(self) -> List[str]:
        return self._addresses

    @property
    def conditions(self) -> Optional[io__k8s__api__discovery__v1__EndpointConditions]:
        return self._conditions

    @property
    def deprecatedTopology(self) -> Optional[Dict[str, str]]:
        return self._deprecatedTopology

    @property
    def hints(self) -> Optional[io__k8s__api__discovery__v1__EndpointHints]:
        return self._hints

    @property
    def hostname(self) -> Optional[str]:
        return self._hostname

    @property
    def nodeName(self) -> Optional[str]:
        return self._nodeName

    @property
    def targetRef(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._targetRef

    @property
    def zone(self) -> Optional[str]:
        return self._zone

    def __init__(
        self,
        addresses: List[str],
        conditions: Optional[io__k8s__api__discovery__v1__EndpointConditions] = None,
        deprecatedTopology: Optional[Dict[str, str]] = None,
        hints: Optional[io__k8s__api__discovery__v1__EndpointHints] = None,
        hostname: Optional[str] = None,
        nodeName: Optional[str] = None,
        targetRef: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        zone: Optional[str] = None,
    ):
        super().__init__()
        if addresses is not None:
            self._addresses = addresses
        if conditions is not None:
            self._conditions = conditions
        if deprecatedTopology is not None:
            self._deprecatedTopology = deprecatedTopology
        if hints is not None:
            self._hints = hints
        if hostname is not None:
            self._hostname = hostname
        if nodeName is not None:
            self._nodeName = nodeName
        if targetRef is not None:
            self._targetRef = targetRef
        if zone is not None:
            self._zone = zone


class io__k8s__api__discovery__v1__EndpointSlice(K8STemplatable):
    """EndpointSlice represents a subset of the endpoints that implement a service. For a given service there may be multiple EndpointSlice objects, selected by labels, which must be joined to produce the full set of endpoints."""

    apiVersion: str = "discovery.k8s.io/v1"
    kind: str = "EndpointSlice"

    props: List[str] = [
        "addressType",
        "apiVersion",
        "endpoints",
        "kind",
        "metadata",
        "ports",
    ]
    required_props: List[str] = ["addressType", "endpoints"]

    @property
    def addressType(self) -> Literal["FQDN", "IPv4", "IPv6"]:
        return self._addressType

    @property
    def endpoints(self) -> List[io__k8s__api__discovery__v1__Endpoint]:
        return self._endpoints

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def ports(self) -> Optional[List[io__k8s__api__discovery__v1__EndpointPort]]:
        return self._ports

    def __init__(
        self,
        addressType: Literal["FQDN", "IPv4", "IPv6"],
        endpoints: List[io__k8s__api__discovery__v1__Endpoint],
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        ports: Optional[List[io__k8s__api__discovery__v1__EndpointPort]] = None,
    ):
        super().__init__()
        if addressType is not None:
            self._addressType = addressType
        if endpoints is not None:
            self._endpoints = endpoints
        if metadata is not None:
            self._metadata = metadata
        if ports is not None:
            self._ports = ports


class io__k8s__api__discovery__v1__EndpointSliceList(K8STemplatable):
    """EndpointSliceList represents a list of endpoint slices"""

    apiVersion: str = "discovery.k8s.io/v1"
    kind: str = "EndpointSliceList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__discovery__v1__EndpointSlice]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__discovery__v1__EndpointSlice],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__discovery__v1beta1__Endpoint(K8STemplatable):
    """Endpoint represents a single logical "backend" implementing a service."""

    props: List[str] = [
        "addresses",
        "conditions",
        "hints",
        "hostname",
        "nodeName",
        "targetRef",
        "topology",
    ]
    required_props: List[str] = ["addresses"]

    @property
    def addresses(self) -> List[str]:
        return self._addresses

    @property
    def conditions(
        self,
    ) -> Optional[io__k8s__api__discovery__v1beta1__EndpointConditions]:
        return self._conditions

    @property
    def hints(self) -> Optional[io__k8s__api__discovery__v1beta1__EndpointHints]:
        return self._hints

    @property
    def hostname(self) -> Optional[str]:
        return self._hostname

    @property
    def nodeName(self) -> Optional[str]:
        return self._nodeName

    @property
    def targetRef(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._targetRef

    @property
    def topology(self) -> Optional[Dict[str, str]]:
        return self._topology

    def __init__(
        self,
        addresses: List[str],
        conditions: Optional[
            io__k8s__api__discovery__v1beta1__EndpointConditions
        ] = None,
        hints: Optional[io__k8s__api__discovery__v1beta1__EndpointHints] = None,
        hostname: Optional[str] = None,
        nodeName: Optional[str] = None,
        targetRef: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        topology: Optional[Dict[str, str]] = None,
    ):
        super().__init__()
        if addresses is not None:
            self._addresses = addresses
        if conditions is not None:
            self._conditions = conditions
        if hints is not None:
            self._hints = hints
        if hostname is not None:
            self._hostname = hostname
        if nodeName is not None:
            self._nodeName = nodeName
        if targetRef is not None:
            self._targetRef = targetRef
        if topology is not None:
            self._topology = topology


class io__k8s__api__discovery__v1beta1__EndpointSlice(K8STemplatable):
    """EndpointSlice represents a subset of the endpoints that implement a service. For a given service there may be multiple EndpointSlice objects, selected by labels, which must be joined to produce the full set of endpoints."""

    apiVersion: str = "discovery.k8s.io/v1beta1"
    kind: str = "EndpointSlice"

    props: List[str] = [
        "addressType",
        "apiVersion",
        "endpoints",
        "kind",
        "metadata",
        "ports",
    ]
    required_props: List[str] = ["addressType", "endpoints"]

    @property
    def addressType(self) -> str:
        return self._addressType

    @property
    def endpoints(self) -> List[io__k8s__api__discovery__v1beta1__Endpoint]:
        return self._endpoints

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def ports(self) -> Optional[List[io__k8s__api__discovery__v1beta1__EndpointPort]]:
        return self._ports

    def __init__(
        self,
        addressType: str,
        endpoints: List[io__k8s__api__discovery__v1beta1__Endpoint],
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        ports: Optional[List[io__k8s__api__discovery__v1beta1__EndpointPort]] = None,
    ):
        super().__init__()
        if addressType is not None:
            self._addressType = addressType
        if endpoints is not None:
            self._endpoints = endpoints
        if metadata is not None:
            self._metadata = metadata
        if ports is not None:
            self._ports = ports


class io__k8s__api__discovery__v1beta1__EndpointSliceList(K8STemplatable):
    """EndpointSliceList represents a list of endpoint slices"""

    apiVersion: str = "discovery.k8s.io/v1beta1"
    kind: str = "EndpointSliceList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__discovery__v1beta1__EndpointSlice]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__discovery__v1beta1__EndpointSlice],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__events__v1__Event(K8STemplatable):
    """Event is a report of an event somewhere in the cluster. It generally denotes some state change in the system. Events have a limited retention time and triggers and messages may evolve with time.  Event consumers should not rely on the timing of an event with a given Reason reflecting a consistent underlying trigger, or the continued existence of events with that Reason.  Events should be treated as informative, best-effort, supplemental data."""

    apiVersion: str = "events.k8s.io/v1"
    kind: str = "Event"

    props: List[str] = [
        "action",
        "apiVersion",
        "deprecatedCount",
        "deprecatedFirstTimestamp",
        "deprecatedLastTimestamp",
        "deprecatedSource",
        "eventTime",
        "kind",
        "metadata",
        "note",
        "reason",
        "regarding",
        "related",
        "reportingController",
        "reportingInstance",
        "series",
        "type",
    ]
    required_props: List[str] = ["eventTime"]

    @property
    def action(self) -> Optional[str]:
        return self._action

    @property
    def deprecatedCount(self) -> Optional[int]:
        return self._deprecatedCount

    @property
    def deprecatedFirstTimestamp(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._deprecatedFirstTimestamp

    @property
    def deprecatedLastTimestamp(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._deprecatedLastTimestamp

    @property
    def deprecatedSource(self) -> Optional[io__k8s__api__core__v1__EventSource]:
        return self._deprecatedSource

    @property
    def eventTime(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime:
        return self._eventTime

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def note(self) -> Optional[str]:
        return self._note

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def regarding(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._regarding

    @property
    def related(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._related

    @property
    def reportingController(self) -> Optional[str]:
        return self._reportingController

    @property
    def reportingInstance(self) -> Optional[str]:
        return self._reportingInstance

    @property
    def series(self) -> Optional[io__k8s__api__events__v1__EventSeries]:
        return self._series

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(
        self,
        eventTime: io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime,
        action: Optional[str] = None,
        deprecatedCount: Optional[int] = None,
        deprecatedFirstTimestamp: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        deprecatedLastTimestamp: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        deprecatedSource: Optional[io__k8s__api__core__v1__EventSource] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        note: Optional[str] = None,
        reason: Optional[str] = None,
        regarding: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        related: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        reportingController: Optional[str] = None,
        reportingInstance: Optional[str] = None,
        series: Optional[io__k8s__api__events__v1__EventSeries] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        if eventTime is not None:
            self._eventTime = eventTime
        if action is not None:
            self._action = action
        if deprecatedCount is not None:
            self._deprecatedCount = deprecatedCount
        if deprecatedFirstTimestamp is not None:
            self._deprecatedFirstTimestamp = deprecatedFirstTimestamp
        if deprecatedLastTimestamp is not None:
            self._deprecatedLastTimestamp = deprecatedLastTimestamp
        if deprecatedSource is not None:
            self._deprecatedSource = deprecatedSource
        if metadata is not None:
            self._metadata = metadata
        if note is not None:
            self._note = note
        if reason is not None:
            self._reason = reason
        if regarding is not None:
            self._regarding = regarding
        if related is not None:
            self._related = related
        if reportingController is not None:
            self._reportingController = reportingController
        if reportingInstance is not None:
            self._reportingInstance = reportingInstance
        if series is not None:
            self._series = series
        if type is not None:
            self._type = type


class io__k8s__api__events__v1__EventList(K8STemplatable):
    """EventList is a list of Event objects."""

    apiVersion: str = "events.k8s.io/v1"
    kind: str = "EventList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__events__v1__Event]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__events__v1__Event],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__events__v1beta1__Event(K8STemplatable):
    """Event is a report of an event somewhere in the cluster. It generally denotes some state change in the system. Events have a limited retention time and triggers and messages may evolve with time.  Event consumers should not rely on the timing of an event with a given Reason reflecting a consistent underlying trigger, or the continued existence of events with that Reason.  Events should be treated as informative, best-effort, supplemental data."""

    apiVersion: str = "events.k8s.io/v1beta1"
    kind: str = "Event"

    props: List[str] = [
        "action",
        "apiVersion",
        "deprecatedCount",
        "deprecatedFirstTimestamp",
        "deprecatedLastTimestamp",
        "deprecatedSource",
        "eventTime",
        "kind",
        "metadata",
        "note",
        "reason",
        "regarding",
        "related",
        "reportingController",
        "reportingInstance",
        "series",
        "type",
    ]
    required_props: List[str] = ["eventTime"]

    @property
    def action(self) -> Optional[str]:
        return self._action

    @property
    def deprecatedCount(self) -> Optional[int]:
        return self._deprecatedCount

    @property
    def deprecatedFirstTimestamp(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._deprecatedFirstTimestamp

    @property
    def deprecatedLastTimestamp(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._deprecatedLastTimestamp

    @property
    def deprecatedSource(self) -> Optional[io__k8s__api__core__v1__EventSource]:
        return self._deprecatedSource

    @property
    def eventTime(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime:
        return self._eventTime

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def note(self) -> Optional[str]:
        return self._note

    @property
    def reason(self) -> Optional[str]:
        return self._reason

    @property
    def regarding(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._regarding

    @property
    def related(self) -> Optional[io__k8s__api__core__v1__ObjectReference]:
        return self._related

    @property
    def reportingController(self) -> Optional[str]:
        return self._reportingController

    @property
    def reportingInstance(self) -> Optional[str]:
        return self._reportingInstance

    @property
    def series(self) -> Optional[io__k8s__api__events__v1beta1__EventSeries]:
        return self._series

    @property
    def type(self) -> Optional[str]:
        return self._type

    def __init__(
        self,
        eventTime: io__k8s__apimachinery__pkg__apis__meta__v1__MicroTime,
        action: Optional[str] = None,
        deprecatedCount: Optional[int] = None,
        deprecatedFirstTimestamp: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        deprecatedLastTimestamp: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        deprecatedSource: Optional[io__k8s__api__core__v1__EventSource] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        note: Optional[str] = None,
        reason: Optional[str] = None,
        regarding: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        related: Optional[io__k8s__api__core__v1__ObjectReference] = None,
        reportingController: Optional[str] = None,
        reportingInstance: Optional[str] = None,
        series: Optional[io__k8s__api__events__v1beta1__EventSeries] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        if eventTime is not None:
            self._eventTime = eventTime
        if action is not None:
            self._action = action
        if deprecatedCount is not None:
            self._deprecatedCount = deprecatedCount
        if deprecatedFirstTimestamp is not None:
            self._deprecatedFirstTimestamp = deprecatedFirstTimestamp
        if deprecatedLastTimestamp is not None:
            self._deprecatedLastTimestamp = deprecatedLastTimestamp
        if deprecatedSource is not None:
            self._deprecatedSource = deprecatedSource
        if metadata is not None:
            self._metadata = metadata
        if note is not None:
            self._note = note
        if reason is not None:
            self._reason = reason
        if regarding is not None:
            self._regarding = regarding
        if related is not None:
            self._related = related
        if reportingController is not None:
            self._reportingController = reportingController
        if reportingInstance is not None:
            self._reportingInstance = reportingInstance
        if series is not None:
            self._series = series
        if type is not None:
            self._type = type


class io__k8s__api__events__v1beta1__EventList(K8STemplatable):
    """EventList is a list of Event objects."""

    apiVersion: str = "events.k8s.io/v1beta1"
    kind: str = "EventList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__events__v1beta1__Event]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__events__v1beta1__Event],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__flowcontrol__v1beta1__PolicyRulesWithSubjects(K8STemplatable):
    """PolicyRulesWithSubjects prescribes a test that applies to a request to an apiserver. The test considers the subject making the request, the verb being requested, and the resource to be acted upon. This PolicyRulesWithSubjects matches a request if and only if both (a) at least one member of subjects matches the request and (b) at least one member of resourceRules or nonResourceRules matches the request."""

    props: List[str] = ["nonResourceRules", "resourceRules", "subjects"]
    required_props: List[str] = ["subjects"]

    @property
    def nonResourceRules(
        self,
    ) -> Optional[List[io__k8s__api__flowcontrol__v1beta1__NonResourcePolicyRule]]:
        return self._nonResourceRules

    @property
    def resourceRules(
        self,
    ) -> Optional[List[io__k8s__api__flowcontrol__v1beta1__ResourcePolicyRule]]:
        return self._resourceRules

    @property
    def subjects(self) -> List[io__k8s__api__flowcontrol__v1beta1__Subject]:
        return self._subjects

    def __init__(
        self,
        subjects: List[io__k8s__api__flowcontrol__v1beta1__Subject],
        nonResourceRules: Optional[
            List[io__k8s__api__flowcontrol__v1beta1__NonResourcePolicyRule]
        ] = None,
        resourceRules: Optional[
            List[io__k8s__api__flowcontrol__v1beta1__ResourcePolicyRule]
        ] = None,
    ):
        super().__init__()
        if subjects is not None:
            self._subjects = subjects
        if nonResourceRules is not None:
            self._nonResourceRules = nonResourceRules
        if resourceRules is not None:
            self._resourceRules = resourceRules


class io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfiguration(K8STemplatable):
    """PriorityLevelConfiguration represents the configuration of a priority level."""

    apiVersion: str = "flowcontrol.apiserver.k8s.io/v1beta1"
    kind: str = "PriorityLevelConfiguration"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationSpec]:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[
            io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationSpec
        ] = None,
        status: Optional[
            io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationStatus
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationList(
    K8STemplatable
):
    """PriorityLevelConfigurationList is a list of PriorityLevelConfiguration objects."""

    apiVersion: str = "flowcontrol.apiserver.k8s.io/v1beta1"
    kind: str = "PriorityLevelConfigurationList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(
        self,
    ) -> List[io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfiguration]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfiguration],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__flowcontrol__v1beta2__PolicyRulesWithSubjects(K8STemplatable):
    """PolicyRulesWithSubjects prescribes a test that applies to a request to an apiserver. The test considers the subject making the request, the verb being requested, and the resource to be acted upon. This PolicyRulesWithSubjects matches a request if and only if both (a) at least one member of subjects matches the request and (b) at least one member of resourceRules or nonResourceRules matches the request."""

    props: List[str] = ["nonResourceRules", "resourceRules", "subjects"]
    required_props: List[str] = ["subjects"]

    @property
    def nonResourceRules(
        self,
    ) -> Optional[List[io__k8s__api__flowcontrol__v1beta2__NonResourcePolicyRule]]:
        return self._nonResourceRules

    @property
    def resourceRules(
        self,
    ) -> Optional[List[io__k8s__api__flowcontrol__v1beta2__ResourcePolicyRule]]:
        return self._resourceRules

    @property
    def subjects(self) -> List[io__k8s__api__flowcontrol__v1beta2__Subject]:
        return self._subjects

    def __init__(
        self,
        subjects: List[io__k8s__api__flowcontrol__v1beta2__Subject],
        nonResourceRules: Optional[
            List[io__k8s__api__flowcontrol__v1beta2__NonResourcePolicyRule]
        ] = None,
        resourceRules: Optional[
            List[io__k8s__api__flowcontrol__v1beta2__ResourcePolicyRule]
        ] = None,
    ):
        super().__init__()
        if subjects is not None:
            self._subjects = subjects
        if nonResourceRules is not None:
            self._nonResourceRules = nonResourceRules
        if resourceRules is not None:
            self._resourceRules = resourceRules


class io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfiguration(K8STemplatable):
    """PriorityLevelConfiguration represents the configuration of a priority level."""

    apiVersion: str = "flowcontrol.apiserver.k8s.io/v1beta2"
    kind: str = "PriorityLevelConfiguration"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationSpec]:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[
            io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationSpec
        ] = None,
        status: Optional[
            io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationStatus
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationList(
    K8STemplatable
):
    """PriorityLevelConfigurationList is a list of PriorityLevelConfiguration objects."""

    apiVersion: str = "flowcontrol.apiserver.k8s.io/v1beta2"
    kind: str = "PriorityLevelConfigurationList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(
        self,
    ) -> List[io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfiguration]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfiguration],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__networking__v1__IngressBackend(K8STemplatable):
    """IngressBackend describes all endpoints for a given service and port."""

    props: List[str] = ["resource", "service"]
    required_props: List[str] = []

    @property
    def resource(self) -> Optional[io__k8s__api__core__v1__TypedLocalObjectReference]:
        return self._resource

    @property
    def service(self) -> Optional[io__k8s__api__networking__v1__IngressServiceBackend]:
        return self._service

    def __init__(
        self,
        resource: Optional[io__k8s__api__core__v1__TypedLocalObjectReference] = None,
        service: Optional[io__k8s__api__networking__v1__IngressServiceBackend] = None,
    ):
        super().__init__()
        if resource is not None:
            self._resource = resource
        if service is not None:
            self._service = service


class io__k8s__api__networking__v1__IngressClass(K8STemplatable):
    """IngressClass represents the class of the Ingress, referenced by the Ingress Spec. The `ingressclass.kubernetes.io/is-default-class` annotation can be used to indicate that an IngressClass should be considered default. When a single IngressClass resource has this annotation set to true, new Ingress resources without a class specified will be assigned this default class."""

    apiVersion: str = "networking.k8s.io/v1"
    kind: str = "IngressClass"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__networking__v1__IngressClassSpec]:
        return self._spec

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__networking__v1__IngressClassSpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec


class io__k8s__api__networking__v1__IngressClassList(K8STemplatable):
    """IngressClassList is a collection of IngressClasses."""

    apiVersion: str = "networking.k8s.io/v1"
    kind: str = "IngressClassList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__networking__v1__IngressClass]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__networking__v1__IngressClass],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__networking__v1__NetworkPolicyPeer(K8STemplatable):
    """NetworkPolicyPeer describes a peer to allow traffic to/from. Only certain combinations of fields are allowed"""

    props: List[str] = ["ipBlock", "namespaceSelector", "podSelector"]
    required_props: List[str] = []

    @property
    def ipBlock(self) -> Optional[io__k8s__api__networking__v1__IPBlock]:
        return self._ipBlock

    @property
    def namespaceSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._namespaceSelector

    @property
    def podSelector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._podSelector

    def __init__(
        self,
        ipBlock: Optional[io__k8s__api__networking__v1__IPBlock] = None,
        namespaceSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        podSelector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if ipBlock is not None:
            self._ipBlock = ipBlock
        if namespaceSelector is not None:
            self._namespaceSelector = namespaceSelector
        if podSelector is not None:
            self._podSelector = podSelector


class io__k8s__api__node__v1__RuntimeClass(K8STemplatable):
    """RuntimeClass defines a class of container runtime supported in the cluster. The RuntimeClass is used to determine which container runtime is used to run all containers in a pod. RuntimeClasses are manually defined by a user or cluster provisioner, and referenced in the PodSpec. The Kubelet is responsible for resolving the RuntimeClassName reference before running the pod.  For more details, see https://kubernetes.io/docs/concepts/containers/runtime-class/"""

    apiVersion: str = "node.k8s.io/v1"
    kind: str = "RuntimeClass"

    props: List[str] = [
        "apiVersion",
        "handler",
        "kind",
        "metadata",
        "overhead",
        "scheduling",
    ]
    required_props: List[str] = ["handler"]

    @property
    def handler(self) -> str:
        return self._handler

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def overhead(self) -> Optional[io__k8s__api__node__v1__Overhead]:
        return self._overhead

    @property
    def scheduling(self) -> Optional[io__k8s__api__node__v1__Scheduling]:
        return self._scheduling

    def __init__(
        self,
        handler: str,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        overhead: Optional[io__k8s__api__node__v1__Overhead] = None,
        scheduling: Optional[io__k8s__api__node__v1__Scheduling] = None,
    ):
        super().__init__()
        if handler is not None:
            self._handler = handler
        if metadata is not None:
            self._metadata = metadata
        if overhead is not None:
            self._overhead = overhead
        if scheduling is not None:
            self._scheduling = scheduling


class io__k8s__api__node__v1__RuntimeClassList(K8STemplatable):
    """RuntimeClassList is a list of RuntimeClass objects."""

    apiVersion: str = "node.k8s.io/v1"
    kind: str = "RuntimeClassList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__node__v1__RuntimeClass]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__node__v1__RuntimeClass],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__node__v1beta1__RuntimeClass(K8STemplatable):
    """RuntimeClass defines a class of container runtime supported in the cluster. The RuntimeClass is used to determine which container runtime is used to run all containers in a pod. RuntimeClasses are (currently) manually defined by a user or cluster provisioner, and referenced in the PodSpec. The Kubelet is responsible for resolving the RuntimeClassName reference before running the pod.  For more details, see https://git.k8s.io/enhancements/keps/sig-node/585-runtime-class"""

    apiVersion: str = "node.k8s.io/v1beta1"
    kind: str = "RuntimeClass"

    props: List[str] = [
        "apiVersion",
        "handler",
        "kind",
        "metadata",
        "overhead",
        "scheduling",
    ]
    required_props: List[str] = ["handler"]

    @property
    def handler(self) -> str:
        return self._handler

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def overhead(self) -> Optional[io__k8s__api__node__v1beta1__Overhead]:
        return self._overhead

    @property
    def scheduling(self) -> Optional[io__k8s__api__node__v1beta1__Scheduling]:
        return self._scheduling

    def __init__(
        self,
        handler: str,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        overhead: Optional[io__k8s__api__node__v1beta1__Overhead] = None,
        scheduling: Optional[io__k8s__api__node__v1beta1__Scheduling] = None,
    ):
        super().__init__()
        if handler is not None:
            self._handler = handler
        if metadata is not None:
            self._metadata = metadata
        if overhead is not None:
            self._overhead = overhead
        if scheduling is not None:
            self._scheduling = scheduling


class io__k8s__api__node__v1beta1__RuntimeClassList(K8STemplatable):
    """RuntimeClassList is a list of RuntimeClass objects."""

    apiVersion: str = "node.k8s.io/v1beta1"
    kind: str = "RuntimeClassList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__node__v1beta1__RuntimeClass]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__node__v1beta1__RuntimeClass],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__policy__v1__Eviction(K8STemplatable):
    """Eviction evicts a pod from its node subject to certain policies and safety constraints. This is a subresource of Pod.  A request to cause such an eviction is created by POSTing to .../pods/<pod name>/evictions."""

    apiVersion: str = "policy/v1"
    kind: str = "Eviction"

    props: List[str] = ["apiVersion", "deleteOptions", "kind", "metadata"]
    required_props: List[str] = []

    @property
    def deleteOptions(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__DeleteOptions]:
        return self._deleteOptions

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    def __init__(
        self,
        deleteOptions: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__DeleteOptions
        ] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if deleteOptions is not None:
            self._deleteOptions = deleteOptions
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__policy__v1__PodDisruptionBudgetSpec(K8STemplatable):
    """PodDisruptionBudgetSpec is a description of a PodDisruptionBudget."""

    props: List[str] = ["maxUnavailable", "minAvailable", "selector"]
    required_props: List[str] = []

    @property
    def maxUnavailable(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._maxUnavailable

    @property
    def minAvailable(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._minAvailable

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    def __init__(
        self,
        maxUnavailable: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
        minAvailable: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if maxUnavailable is not None:
            self._maxUnavailable = maxUnavailable
        if minAvailable is not None:
            self._minAvailable = minAvailable
        if selector is not None:
            self._selector = selector


class io__k8s__api__policy__v1__PodDisruptionBudgetStatus(K8STemplatable):
    """PodDisruptionBudgetStatus represents information about the status of a PodDisruptionBudget. Status may trail the actual state of a system."""

    props: List[str] = [
        "conditions",
        "currentHealthy",
        "desiredHealthy",
        "disruptedPods",
        "disruptionsAllowed",
        "expectedPods",
        "observedGeneration",
    ]
    required_props: List[str] = [
        "disruptionsAllowed",
        "currentHealthy",
        "desiredHealthy",
        "expectedPods",
    ]

    @property
    def conditions(
        self,
    ) -> Optional[List[io__k8s__apimachinery__pkg__apis__meta__v1__Condition]]:
        return self._conditions

    @property
    def currentHealthy(self) -> int:
        return self._currentHealthy

    @property
    def desiredHealthy(self) -> int:
        return self._desiredHealthy

    @property
    def disruptedPods(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__apis__meta__v1__Time]]:
        return self._disruptedPods

    @property
    def disruptionsAllowed(self) -> int:
        return self._disruptionsAllowed

    @property
    def expectedPods(self) -> int:
        return self._expectedPods

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    def __init__(
        self,
        currentHealthy: int,
        desiredHealthy: int,
        disruptionsAllowed: int,
        expectedPods: int,
        conditions: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__Condition]
        ] = None,
        disruptedPods: Optional[
            Dict[str, io__k8s__apimachinery__pkg__apis__meta__v1__Time]
        ] = None,
        observedGeneration: Optional[int] = None,
    ):
        super().__init__()
        if currentHealthy is not None:
            self._currentHealthy = currentHealthy
        if desiredHealthy is not None:
            self._desiredHealthy = desiredHealthy
        if disruptionsAllowed is not None:
            self._disruptionsAllowed = disruptionsAllowed
        if expectedPods is not None:
            self._expectedPods = expectedPods
        if conditions is not None:
            self._conditions = conditions
        if disruptedPods is not None:
            self._disruptedPods = disruptedPods
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration


class io__k8s__api__policy__v1beta1__PodDisruptionBudgetSpec(K8STemplatable):
    """PodDisruptionBudgetSpec is a description of a PodDisruptionBudget."""

    props: List[str] = ["maxUnavailable", "minAvailable", "selector"]
    required_props: List[str] = []

    @property
    def maxUnavailable(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._maxUnavailable

    @property
    def minAvailable(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__util__intstr__IntOrString]:
        return self._minAvailable

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    def __init__(
        self,
        maxUnavailable: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
        minAvailable: Optional[
            io__k8s__apimachinery__pkg__util__intstr__IntOrString
        ] = None,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if maxUnavailable is not None:
            self._maxUnavailable = maxUnavailable
        if minAvailable is not None:
            self._minAvailable = minAvailable
        if selector is not None:
            self._selector = selector


class io__k8s__api__policy__v1beta1__PodDisruptionBudgetStatus(K8STemplatable):
    """PodDisruptionBudgetStatus represents information about the status of a PodDisruptionBudget. Status may trail the actual state of a system."""

    props: List[str] = [
        "conditions",
        "currentHealthy",
        "desiredHealthy",
        "disruptedPods",
        "disruptionsAllowed",
        "expectedPods",
        "observedGeneration",
    ]
    required_props: List[str] = [
        "disruptionsAllowed",
        "currentHealthy",
        "desiredHealthy",
        "expectedPods",
    ]

    @property
    def conditions(
        self,
    ) -> Optional[List[io__k8s__apimachinery__pkg__apis__meta__v1__Condition]]:
        return self._conditions

    @property
    def currentHealthy(self) -> int:
        return self._currentHealthy

    @property
    def desiredHealthy(self) -> int:
        return self._desiredHealthy

    @property
    def disruptedPods(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__apis__meta__v1__Time]]:
        return self._disruptedPods

    @property
    def disruptionsAllowed(self) -> int:
        return self._disruptionsAllowed

    @property
    def expectedPods(self) -> int:
        return self._expectedPods

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    def __init__(
        self,
        currentHealthy: int,
        desiredHealthy: int,
        disruptionsAllowed: int,
        expectedPods: int,
        conditions: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__Condition]
        ] = None,
        disruptedPods: Optional[
            Dict[str, io__k8s__apimachinery__pkg__apis__meta__v1__Time]
        ] = None,
        observedGeneration: Optional[int] = None,
    ):
        super().__init__()
        if currentHealthy is not None:
            self._currentHealthy = currentHealthy
        if desiredHealthy is not None:
            self._desiredHealthy = desiredHealthy
        if disruptionsAllowed is not None:
            self._disruptionsAllowed = disruptionsAllowed
        if expectedPods is not None:
            self._expectedPods = expectedPods
        if conditions is not None:
            self._conditions = conditions
        if disruptedPods is not None:
            self._disruptedPods = disruptedPods
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration


class io__k8s__api__policy__v1beta1__PodSecurityPolicy(K8STemplatable):
    """PodSecurityPolicy governs the ability to make requests that affect the Security Context that will be applied to a pod and container. Deprecated in 1.21."""

    apiVersion: str = "policy/v1beta1"
    kind: str = "PodSecurityPolicy"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__policy__v1beta1__PodSecurityPolicySpec]:
        return self._spec

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__policy__v1beta1__PodSecurityPolicySpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec


class io__k8s__api__policy__v1beta1__PodSecurityPolicyList(K8STemplatable):
    """PodSecurityPolicyList is a list of PodSecurityPolicy objects."""

    apiVersion: str = "policy/v1beta1"
    kind: str = "PodSecurityPolicyList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__policy__v1beta1__PodSecurityPolicy]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__policy__v1beta1__PodSecurityPolicy],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__rbac__v1__AggregationRule(K8STemplatable):
    """AggregationRule describes how to locate ClusterRoles to aggregate into the ClusterRole"""

    props: List[str] = ["clusterRoleSelectors"]
    required_props: List[str] = []

    @property
    def clusterRoleSelectors(
        self,
    ) -> Optional[List[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]]:
        return self._clusterRoleSelectors

    def __init__(
        self,
        clusterRoleSelectors: Optional[
            List[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]
        ] = None,
    ):
        super().__init__()
        if clusterRoleSelectors is not None:
            self._clusterRoleSelectors = clusterRoleSelectors


class io__k8s__api__rbac__v1__ClusterRole(K8STemplatable):
    """ClusterRole is a cluster level, logical grouping of PolicyRules that can be referenced as a unit by a RoleBinding or ClusterRoleBinding."""

    apiVersion: str = "rbac.authorization.k8s.io/v1"
    kind: str = "ClusterRole"

    props: List[str] = ["aggregationRule", "apiVersion", "kind", "metadata", "rules"]
    required_props: List[str] = []

    @property
    def aggregationRule(self) -> Optional[io__k8s__api__rbac__v1__AggregationRule]:
        return self._aggregationRule

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def rules(self) -> Optional[List[io__k8s__api__rbac__v1__PolicyRule]]:
        return self._rules

    def __init__(
        self,
        aggregationRule: Optional[io__k8s__api__rbac__v1__AggregationRule] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        rules: Optional[List[io__k8s__api__rbac__v1__PolicyRule]] = None,
    ):
        super().__init__()
        if aggregationRule is not None:
            self._aggregationRule = aggregationRule
        if metadata is not None:
            self._metadata = metadata
        if rules is not None:
            self._rules = rules


class io__k8s__api__rbac__v1__ClusterRoleBinding(K8STemplatable):
    """ClusterRoleBinding references a ClusterRole, but not contain it.  It can reference a ClusterRole in the global namespace, and adds who information via Subject."""

    apiVersion: str = "rbac.authorization.k8s.io/v1"
    kind: str = "ClusterRoleBinding"

    props: List[str] = ["apiVersion", "kind", "metadata", "roleRef", "subjects"]
    required_props: List[str] = ["roleRef"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def roleRef(self) -> io__k8s__api__rbac__v1__RoleRef:
        return self._roleRef

    @property
    def subjects(self) -> Optional[List[io__k8s__api__rbac__v1__Subject]]:
        return self._subjects

    def __init__(
        self,
        roleRef: io__k8s__api__rbac__v1__RoleRef,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        subjects: Optional[List[io__k8s__api__rbac__v1__Subject]] = None,
    ):
        super().__init__()
        if roleRef is not None:
            self._roleRef = roleRef
        if metadata is not None:
            self._metadata = metadata
        if subjects is not None:
            self._subjects = subjects


class io__k8s__api__rbac__v1__ClusterRoleBindingList(K8STemplatable):
    """ClusterRoleBindingList is a collection of ClusterRoleBindings"""

    apiVersion: str = "rbac.authorization.k8s.io/v1"
    kind: str = "ClusterRoleBindingList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__rbac__v1__ClusterRoleBinding]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__rbac__v1__ClusterRoleBinding],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__rbac__v1__ClusterRoleList(K8STemplatable):
    """ClusterRoleList is a collection of ClusterRoles"""

    apiVersion: str = "rbac.authorization.k8s.io/v1"
    kind: str = "ClusterRoleList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__rbac__v1__ClusterRole]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__rbac__v1__ClusterRole],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__rbac__v1__Role(K8STemplatable):
    """Role is a namespaced, logical grouping of PolicyRules that can be referenced as a unit by a RoleBinding."""

    apiVersion: str = "rbac.authorization.k8s.io/v1"
    kind: str = "Role"

    props: List[str] = ["apiVersion", "kind", "metadata", "rules"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def rules(self) -> Optional[List[io__k8s__api__rbac__v1__PolicyRule]]:
        return self._rules

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        rules: Optional[List[io__k8s__api__rbac__v1__PolicyRule]] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if rules is not None:
            self._rules = rules


class io__k8s__api__rbac__v1__RoleBinding(K8STemplatable):
    """RoleBinding references a role, but does not contain it.  It can reference a Role in the same namespace or a ClusterRole in the global namespace. It adds who information via Subjects and namespace information by which namespace it exists in.  RoleBindings in a given namespace only have effect in that namespace."""

    apiVersion: str = "rbac.authorization.k8s.io/v1"
    kind: str = "RoleBinding"

    props: List[str] = ["apiVersion", "kind", "metadata", "roleRef", "subjects"]
    required_props: List[str] = ["roleRef"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def roleRef(self) -> io__k8s__api__rbac__v1__RoleRef:
        return self._roleRef

    @property
    def subjects(self) -> Optional[List[io__k8s__api__rbac__v1__Subject]]:
        return self._subjects

    def __init__(
        self,
        roleRef: io__k8s__api__rbac__v1__RoleRef,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        subjects: Optional[List[io__k8s__api__rbac__v1__Subject]] = None,
    ):
        super().__init__()
        if roleRef is not None:
            self._roleRef = roleRef
        if metadata is not None:
            self._metadata = metadata
        if subjects is not None:
            self._subjects = subjects


class io__k8s__api__rbac__v1__RoleBindingList(K8STemplatable):
    """RoleBindingList is a collection of RoleBindings"""

    apiVersion: str = "rbac.authorization.k8s.io/v1"
    kind: str = "RoleBindingList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__rbac__v1__RoleBinding]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__rbac__v1__RoleBinding],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__rbac__v1__RoleList(K8STemplatable):
    """RoleList is a collection of Roles"""

    apiVersion: str = "rbac.authorization.k8s.io/v1"
    kind: str = "RoleList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__rbac__v1__Role]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__rbac__v1__Role],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__scheduling__v1__PriorityClass(K8STemplatable):
    """PriorityClass defines mapping from a priority class name to the priority integer value. The value can be any valid integer."""

    apiVersion: str = "scheduling.k8s.io/v1"
    kind: str = "PriorityClass"

    props: List[str] = [
        "apiVersion",
        "description",
        "globalDefault",
        "kind",
        "metadata",
        "preemptionPolicy",
        "value",
    ]
    required_props: List[str] = ["value"]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def globalDefault(self) -> Optional[bool]:
        return self._globalDefault

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def preemptionPolicy(self) -> Optional[str]:
        return self._preemptionPolicy

    @property
    def value(self) -> int:
        return self._value

    def __init__(
        self,
        value: int,
        description: Optional[str] = None,
        globalDefault: Optional[bool] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        preemptionPolicy: Optional[str] = None,
    ):
        super().__init__()
        if value is not None:
            self._value = value
        if description is not None:
            self._description = description
        if globalDefault is not None:
            self._globalDefault = globalDefault
        if metadata is not None:
            self._metadata = metadata
        if preemptionPolicy is not None:
            self._preemptionPolicy = preemptionPolicy


class io__k8s__api__scheduling__v1__PriorityClassList(K8STemplatable):
    """PriorityClassList is a collection of priority classes."""

    apiVersion: str = "scheduling.k8s.io/v1"
    kind: str = "PriorityClassList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__scheduling__v1__PriorityClass]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__scheduling__v1__PriorityClass],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1__CSIDriver(K8STemplatable):
    """CSIDriver captures information about a Container Storage Interface (CSI) volume driver deployed on the cluster. Kubernetes attach detach controller uses this object to determine whether attach is required. Kubelet uses this object to determine whether pod information needs to be passed on mount. CSIDriver objects are non-namespaced."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "CSIDriver"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__storage__v1__CSIDriverSpec:
        return self._spec

    def __init__(
        self,
        spec: io__k8s__api__storage__v1__CSIDriverSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1__CSIDriverList(K8STemplatable):
    """CSIDriverList is a collection of CSIDriver objects."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "CSIDriverList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__storage__v1__CSIDriver]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__storage__v1__CSIDriver],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1__CSINode(K8STemplatable):
    """CSINode holds information about all CSI drivers installed on a node. CSI drivers do not need to create the CSINode object directly. As long as they use the node-driver-registrar sidecar container, the kubelet will automatically populate the CSINode object for the CSI driver as part of kubelet plugin registration. CSINode has the same name as a node. If the object is missing, it means either there are no CSI Drivers available on the node, or the Kubelet version is low enough that it doesn't create this object. CSINode has an OwnerReference that points to the corresponding node object."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "CSINode"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__storage__v1__CSINodeSpec:
        return self._spec

    def __init__(
        self,
        spec: io__k8s__api__storage__v1__CSINodeSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1__CSINodeList(K8STemplatable):
    """CSINodeList is a collection of CSINode objects."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "CSINodeList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__storage__v1__CSINode]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__storage__v1__CSINode],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1__CSIStorageCapacity(K8STemplatable):
    """CSIStorageCapacity stores the result of one CSI GetCapacity call. For a given StorageClass, this describes the available capacity in a particular topology segment.  This can be used when considering where to instantiate new PersistentVolumes.

    For example this can express things like: - StorageClass "standard" has "1234 GiB" available in "topology.kubernetes.io/zone=us-east1" - StorageClass "localssd" has "10 GiB" available in "kubernetes.io/hostname=knode-abc123"

    The following three cases all imply that no capacity is available for a certain combination: - no object exists with suitable topology and storage class name - such an object exists, but the capacity is unset - such an object exists, but the capacity is zero

    The producer of these objects can decide which approach is more suitable.

    They are consumed by the kube-scheduler when a CSI driver opts into capacity-aware scheduling with CSIDriverSpec.StorageCapacity. The scheduler compares the MaximumVolumeSize against the requested size of pending volumes to filter out unsuitable nodes. If MaximumVolumeSize is unset, it falls back to a comparison against the less precise Capacity. If that is also unset, the scheduler assumes that capacity is insufficient and tries some other node."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "CSIStorageCapacity"

    props: List[str] = [
        "apiVersion",
        "capacity",
        "kind",
        "maximumVolumeSize",
        "metadata",
        "nodeTopology",
        "storageClassName",
    ]
    required_props: List[str] = ["storageClassName"]

    @property
    def capacity(self) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._capacity

    @property
    def maximumVolumeSize(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._maximumVolumeSize

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def nodeTopology(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._nodeTopology

    @property
    def storageClassName(self) -> str:
        return self._storageClassName

    def __init__(
        self,
        storageClassName: str,
        capacity: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
        maximumVolumeSize: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        nodeTopology: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if storageClassName is not None:
            self._storageClassName = storageClassName
        if capacity is not None:
            self._capacity = capacity
        if maximumVolumeSize is not None:
            self._maximumVolumeSize = maximumVolumeSize
        if metadata is not None:
            self._metadata = metadata
        if nodeTopology is not None:
            self._nodeTopology = nodeTopology


class io__k8s__api__storage__v1__CSIStorageCapacityList(K8STemplatable):
    """CSIStorageCapacityList is a collection of CSIStorageCapacity objects."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "CSIStorageCapacityList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__storage__v1__CSIStorageCapacity]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__storage__v1__CSIStorageCapacity],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1__StorageClass(K8STemplatable):
    """StorageClass describes the parameters for a class of storage for which PersistentVolumes can be dynamically provisioned.

    StorageClasses are non-namespaced; the name of the storage class according to etcd is in ObjectMeta.Name."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "StorageClass"

    props: List[str] = [
        "allowVolumeExpansion",
        "allowedTopologies",
        "apiVersion",
        "kind",
        "metadata",
        "mountOptions",
        "parameters",
        "provisioner",
        "reclaimPolicy",
        "volumeBindingMode",
    ]
    required_props: List[str] = ["provisioner"]

    @property
    def allowVolumeExpansion(self) -> Optional[bool]:
        return self._allowVolumeExpansion

    @property
    def allowedTopologies(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__TopologySelectorTerm]]:
        return self._allowedTopologies

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def mountOptions(self) -> Optional[List[str]]:
        return self._mountOptions

    @property
    def parameters(self) -> Optional[Dict[str, str]]:
        return self._parameters

    @property
    def provisioner(self) -> str:
        return self._provisioner

    @property
    def reclaimPolicy(self) -> Optional[str]:
        return self._reclaimPolicy

    @property
    def volumeBindingMode(self) -> Optional[str]:
        return self._volumeBindingMode

    def __init__(
        self,
        provisioner: str,
        allowVolumeExpansion: Optional[bool] = None,
        allowedTopologies: Optional[
            List[io__k8s__api__core__v1__TopologySelectorTerm]
        ] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        mountOptions: Optional[List[str]] = None,
        parameters: Optional[Dict[str, str]] = None,
        reclaimPolicy: Optional[str] = None,
        volumeBindingMode: Optional[str] = None,
    ):
        super().__init__()
        if provisioner is not None:
            self._provisioner = provisioner
        if allowVolumeExpansion is not None:
            self._allowVolumeExpansion = allowVolumeExpansion
        if allowedTopologies is not None:
            self._allowedTopologies = allowedTopologies
        if metadata is not None:
            self._metadata = metadata
        if mountOptions is not None:
            self._mountOptions = mountOptions
        if parameters is not None:
            self._parameters = parameters
        if reclaimPolicy is not None:
            self._reclaimPolicy = reclaimPolicy
        if volumeBindingMode is not None:
            self._volumeBindingMode = volumeBindingMode


class io__k8s__api__storage__v1__StorageClassList(K8STemplatable):
    """StorageClassList is a collection of storage classes."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "StorageClassList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__storage__v1__StorageClass]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__storage__v1__StorageClass],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1__VolumeAttachmentSource(K8STemplatable):
    """VolumeAttachmentSource represents a volume that should be attached. Right now only PersistenVolumes can be attached via external attacher, in future we may allow also inline volumes in pods. Exactly one member can be set."""

    props: List[str] = ["inlineVolumeSpec", "persistentVolumeName"]
    required_props: List[str] = []

    @property
    def inlineVolumeSpec(
        self,
    ) -> Optional[io__k8s__api__core__v1__PersistentVolumeSpec]:
        return self._inlineVolumeSpec

    @property
    def persistentVolumeName(self) -> Optional[str]:
        return self._persistentVolumeName

    def __init__(
        self,
        inlineVolumeSpec: Optional[io__k8s__api__core__v1__PersistentVolumeSpec] = None,
        persistentVolumeName: Optional[str] = None,
    ):
        super().__init__()
        if inlineVolumeSpec is not None:
            self._inlineVolumeSpec = inlineVolumeSpec
        if persistentVolumeName is not None:
            self._persistentVolumeName = persistentVolumeName


class io__k8s__api__storage__v1__VolumeAttachmentSpec(K8STemplatable):
    """VolumeAttachmentSpec is the specification of a VolumeAttachment request."""

    props: List[str] = ["attacher", "nodeName", "source"]
    required_props: List[str] = ["attacher", "source", "nodeName"]

    @property
    def attacher(self) -> str:
        return self._attacher

    @property
    def nodeName(self) -> str:
        return self._nodeName

    @property
    def source(self) -> io__k8s__api__storage__v1__VolumeAttachmentSource:
        return self._source

    def __init__(
        self,
        attacher: str,
        nodeName: str,
        source: io__k8s__api__storage__v1__VolumeAttachmentSource,
    ):
        super().__init__()
        if attacher is not None:
            self._attacher = attacher
        if nodeName is not None:
            self._nodeName = nodeName
        if source is not None:
            self._source = source


class io__k8s__api__storage__v1__VolumeAttachmentStatus(K8STemplatable):
    """VolumeAttachmentStatus is the status of a VolumeAttachment request."""

    props: List[str] = ["attachError", "attached", "attachmentMetadata", "detachError"]
    required_props: List[str] = ["attached"]

    @property
    def attachError(self) -> Optional[io__k8s__api__storage__v1__VolumeError]:
        return self._attachError

    @property
    def attached(self) -> bool:
        return self._attached

    @property
    def attachmentMetadata(self) -> Optional[Dict[str, str]]:
        return self._attachmentMetadata

    @property
    def detachError(self) -> Optional[io__k8s__api__storage__v1__VolumeError]:
        return self._detachError

    def __init__(
        self,
        attached: bool,
        attachError: Optional[io__k8s__api__storage__v1__VolumeError] = None,
        attachmentMetadata: Optional[Dict[str, str]] = None,
        detachError: Optional[io__k8s__api__storage__v1__VolumeError] = None,
    ):
        super().__init__()
        if attached is not None:
            self._attached = attached
        if attachError is not None:
            self._attachError = attachError
        if attachmentMetadata is not None:
            self._attachmentMetadata = attachmentMetadata
        if detachError is not None:
            self._detachError = detachError


class io__k8s__api__storage__v1alpha1__CSIStorageCapacity(K8STemplatable):
    """CSIStorageCapacity stores the result of one CSI GetCapacity call. For a given StorageClass, this describes the available capacity in a particular topology segment.  This can be used when considering where to instantiate new PersistentVolumes.

    For example this can express things like: - StorageClass "standard" has "1234 GiB" available in "topology.kubernetes.io/zone=us-east1" - StorageClass "localssd" has "10 GiB" available in "kubernetes.io/hostname=knode-abc123"

    The following three cases all imply that no capacity is available for a certain combination: - no object exists with suitable topology and storage class name - such an object exists, but the capacity is unset - such an object exists, but the capacity is zero

    The producer of these objects can decide which approach is more suitable.

    They are consumed by the kube-scheduler when a CSI driver opts into capacity-aware scheduling with CSIDriverSpec.StorageCapacity. The scheduler compares the MaximumVolumeSize against the requested size of pending volumes to filter out unsuitable nodes. If MaximumVolumeSize is unset, it falls back to a comparison against the less precise Capacity. If that is also unset, the scheduler assumes that capacity is insufficient and tries some other node."""

    apiVersion: str = "storage.k8s.io/v1alpha1"
    kind: str = "CSIStorageCapacity"

    props: List[str] = [
        "apiVersion",
        "capacity",
        "kind",
        "maximumVolumeSize",
        "metadata",
        "nodeTopology",
        "storageClassName",
    ]
    required_props: List[str] = ["storageClassName"]

    @property
    def capacity(self) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._capacity

    @property
    def maximumVolumeSize(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._maximumVolumeSize

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def nodeTopology(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._nodeTopology

    @property
    def storageClassName(self) -> str:
        return self._storageClassName

    def __init__(
        self,
        storageClassName: str,
        capacity: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
        maximumVolumeSize: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        nodeTopology: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if storageClassName is not None:
            self._storageClassName = storageClassName
        if capacity is not None:
            self._capacity = capacity
        if maximumVolumeSize is not None:
            self._maximumVolumeSize = maximumVolumeSize
        if metadata is not None:
            self._metadata = metadata
        if nodeTopology is not None:
            self._nodeTopology = nodeTopology


class io__k8s__api__storage__v1alpha1__CSIStorageCapacityList(K8STemplatable):
    """CSIStorageCapacityList is a collection of CSIStorageCapacity objects."""

    apiVersion: str = "storage.k8s.io/v1alpha1"
    kind: str = "CSIStorageCapacityList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__storage__v1alpha1__CSIStorageCapacity]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__storage__v1alpha1__CSIStorageCapacity],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1beta1__CSIStorageCapacity(K8STemplatable):
    """CSIStorageCapacity stores the result of one CSI GetCapacity call. For a given StorageClass, this describes the available capacity in a particular topology segment.  This can be used when considering where to instantiate new PersistentVolumes.

    For example this can express things like: - StorageClass "standard" has "1234 GiB" available in "topology.kubernetes.io/zone=us-east1" - StorageClass "localssd" has "10 GiB" available in "kubernetes.io/hostname=knode-abc123"

    The following three cases all imply that no capacity is available for a certain combination: - no object exists with suitable topology and storage class name - such an object exists, but the capacity is unset - such an object exists, but the capacity is zero

    The producer of these objects can decide which approach is more suitable.

    They are consumed by the kube-scheduler when a CSI driver opts into capacity-aware scheduling with CSIDriverSpec.StorageCapacity. The scheduler compares the MaximumVolumeSize against the requested size of pending volumes to filter out unsuitable nodes. If MaximumVolumeSize is unset, it falls back to a comparison against the less precise Capacity. If that is also unset, the scheduler assumes that capacity is insufficient and tries some other node."""

    apiVersion: str = "storage.k8s.io/v1beta1"
    kind: str = "CSIStorageCapacity"

    props: List[str] = [
        "apiVersion",
        "capacity",
        "kind",
        "maximumVolumeSize",
        "metadata",
        "nodeTopology",
        "storageClassName",
    ]
    required_props: List[str] = ["storageClassName"]

    @property
    def capacity(self) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._capacity

    @property
    def maximumVolumeSize(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__api__resource__Quantity]:
        return self._maximumVolumeSize

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def nodeTopology(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._nodeTopology

    @property
    def storageClassName(self) -> str:
        return self._storageClassName

    def __init__(
        self,
        storageClassName: str,
        capacity: Optional[io__k8s__apimachinery__pkg__api__resource__Quantity] = None,
        maximumVolumeSize: Optional[
            io__k8s__apimachinery__pkg__api__resource__Quantity
        ] = None,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        nodeTopology: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
    ):
        super().__init__()
        if storageClassName is not None:
            self._storageClassName = storageClassName
        if capacity is not None:
            self._capacity = capacity
        if maximumVolumeSize is not None:
            self._maximumVolumeSize = maximumVolumeSize
        if metadata is not None:
            self._metadata = metadata
        if nodeTopology is not None:
            self._nodeTopology = nodeTopology


class io__k8s__api__storage__v1beta1__CSIStorageCapacityList(K8STemplatable):
    """CSIStorageCapacityList is a collection of CSIStorageCapacity objects."""

    apiVersion: str = "storage.k8s.io/v1beta1"
    kind: str = "CSIStorageCapacityList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__storage__v1beta1__CSIStorageCapacity]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__storage__v1beta1__CSIStorageCapacity],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceValidation(
    K8STemplatable
):
    """CustomResourceValidation is a list of validation methods for CustomResources."""

    props: List[str] = ["openAPIV3Schema"]
    required_props: List[str] = []

    @property
    def openAPIV3Schema(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaProps
    ]:
        return self._openAPIV3Schema

    def __init__(
        self,
        openAPIV3Schema: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaProps
        ] = None,
    ):
        super().__init__()
        if openAPIV3Schema is not None:
            self._openAPIV3Schema = openAPIV3Schema


class io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIService(
    K8STemplatable
):
    """APIService represents a server for a particular GroupVersion. Name must be "version.group"."""

    apiVersion: str = "apiregistration.k8s.io/v1"
    kind: str = "APIService"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(
        self,
    ) -> Optional[
        io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceSpec
    ]:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[
        io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceStatus
    ]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[
            io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceSpec
        ] = None,
        status: Optional[
            io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceStatus
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceList(
    K8STemplatable
):
    """APIServiceList is a list of APIService objects."""

    apiVersion: str = "apiregistration.k8s.io/v1"
    kind: str = "APIServiceList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(
        self,
    ) -> List[io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIService]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[
            io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIService
        ],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__autoscaling__v2__ExternalMetricSource(K8STemplatable):
    """ExternalMetricSource indicates how to scale on a metric not associated with any Kubernetes object (for example length of queue in cloud messaging service, or QPS from loadbalancer running outside of cluster)."""

    props: List[str] = ["metric", "target"]
    required_props: List[str] = ["metric", "target"]

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2__MetricIdentifier:
        return self._metric

    @property
    def target(self) -> io__k8s__api__autoscaling__v2__MetricTarget:
        return self._target

    def __init__(
        self,
        metric: io__k8s__api__autoscaling__v2__MetricIdentifier,
        target: io__k8s__api__autoscaling__v2__MetricTarget,
    ):
        super().__init__()
        if metric is not None:
            self._metric = metric
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2__ExternalMetricStatus(K8STemplatable):
    """ExternalMetricStatus indicates the current value of a global metric not associated with any Kubernetes object."""

    props: List[str] = ["current", "metric"]
    required_props: List[str] = ["metric", "current"]

    @property
    def current(self) -> io__k8s__api__autoscaling__v2__MetricValueStatus:
        return self._current

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2__MetricIdentifier:
        return self._metric

    def __init__(
        self,
        current: io__k8s__api__autoscaling__v2__MetricValueStatus,
        metric: io__k8s__api__autoscaling__v2__MetricIdentifier,
    ):
        super().__init__()
        if current is not None:
            self._current = current
        if metric is not None:
            self._metric = metric


class io__k8s__api__autoscaling__v2__MetricSpec(K8STemplatable):
    """MetricSpec specifies how to scale based on a single metric (only `type` and one other matching field should be set at once)."""

    props: List[str] = [
        "containerResource",
        "external",
        "object",
        "pods",
        "resource",
        "type",
    ]
    required_props: List[str] = ["type"]

    @property
    def containerResource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2__ContainerResourceMetricSource]:
        return self._containerResource

    @property
    def external(self) -> Optional[io__k8s__api__autoscaling__v2__ExternalMetricSource]:
        return self._external

    @property
    def object(self) -> Optional[io__k8s__api__autoscaling__v2__ObjectMetricSource]:
        return self._object

    @property
    def pods(self) -> Optional[io__k8s__api__autoscaling__v2__PodsMetricSource]:
        return self._pods

    @property
    def resource(self) -> Optional[io__k8s__api__autoscaling__v2__ResourceMetricSource]:
        return self._resource

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        containerResource: Optional[
            io__k8s__api__autoscaling__v2__ContainerResourceMetricSource
        ] = None,
        external: Optional[io__k8s__api__autoscaling__v2__ExternalMetricSource] = None,
        object: Optional[io__k8s__api__autoscaling__v2__ObjectMetricSource] = None,
        pods: Optional[io__k8s__api__autoscaling__v2__PodsMetricSource] = None,
        resource: Optional[io__k8s__api__autoscaling__v2__ResourceMetricSource] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if containerResource is not None:
            self._containerResource = containerResource
        if external is not None:
            self._external = external
        if object is not None:
            self._object = object
        if pods is not None:
            self._pods = pods
        if resource is not None:
            self._resource = resource


class io__k8s__api__autoscaling__v2__MetricStatus(K8STemplatable):
    """MetricStatus describes the last-read state of a single metric."""

    props: List[str] = [
        "containerResource",
        "external",
        "object",
        "pods",
        "resource",
        "type",
    ]
    required_props: List[str] = ["type"]

    @property
    def containerResource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2__ContainerResourceMetricStatus]:
        return self._containerResource

    @property
    def external(self) -> Optional[io__k8s__api__autoscaling__v2__ExternalMetricStatus]:
        return self._external

    @property
    def object(self) -> Optional[io__k8s__api__autoscaling__v2__ObjectMetricStatus]:
        return self._object

    @property
    def pods(self) -> Optional[io__k8s__api__autoscaling__v2__PodsMetricStatus]:
        return self._pods

    @property
    def resource(self) -> Optional[io__k8s__api__autoscaling__v2__ResourceMetricStatus]:
        return self._resource

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        containerResource: Optional[
            io__k8s__api__autoscaling__v2__ContainerResourceMetricStatus
        ] = None,
        external: Optional[io__k8s__api__autoscaling__v2__ExternalMetricStatus] = None,
        object: Optional[io__k8s__api__autoscaling__v2__ObjectMetricStatus] = None,
        pods: Optional[io__k8s__api__autoscaling__v2__PodsMetricStatus] = None,
        resource: Optional[io__k8s__api__autoscaling__v2__ResourceMetricStatus] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if containerResource is not None:
            self._containerResource = containerResource
        if external is not None:
            self._external = external
        if object is not None:
            self._object = object
        if pods is not None:
            self._pods = pods
        if resource is not None:
            self._resource = resource


class io__k8s__api__autoscaling__v2beta1__MetricSpec(K8STemplatable):
    """MetricSpec specifies how to scale based on a single metric (only `type` and one other matching field should be set at once)."""

    props: List[str] = [
        "containerResource",
        "external",
        "object",
        "pods",
        "resource",
        "type",
    ]
    required_props: List[str] = ["type"]

    @property
    def containerResource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__ContainerResourceMetricSource]:
        return self._containerResource

    @property
    def external(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__ExternalMetricSource]:
        return self._external

    @property
    def object(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__ObjectMetricSource]:
        return self._object

    @property
    def pods(self) -> Optional[io__k8s__api__autoscaling__v2beta1__PodsMetricSource]:
        return self._pods

    @property
    def resource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__ResourceMetricSource]:
        return self._resource

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        containerResource: Optional[
            io__k8s__api__autoscaling__v2beta1__ContainerResourceMetricSource
        ] = None,
        external: Optional[
            io__k8s__api__autoscaling__v2beta1__ExternalMetricSource
        ] = None,
        object: Optional[io__k8s__api__autoscaling__v2beta1__ObjectMetricSource] = None,
        pods: Optional[io__k8s__api__autoscaling__v2beta1__PodsMetricSource] = None,
        resource: Optional[
            io__k8s__api__autoscaling__v2beta1__ResourceMetricSource
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if containerResource is not None:
            self._containerResource = containerResource
        if external is not None:
            self._external = external
        if object is not None:
            self._object = object
        if pods is not None:
            self._pods = pods
        if resource is not None:
            self._resource = resource


class io__k8s__api__autoscaling__v2beta1__MetricStatus(K8STemplatable):
    """MetricStatus describes the last-read state of a single metric."""

    props: List[str] = [
        "containerResource",
        "external",
        "object",
        "pods",
        "resource",
        "type",
    ]
    required_props: List[str] = ["type"]

    @property
    def containerResource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__ContainerResourceMetricStatus]:
        return self._containerResource

    @property
    def external(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__ExternalMetricStatus]:
        return self._external

    @property
    def object(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__ObjectMetricStatus]:
        return self._object

    @property
    def pods(self) -> Optional[io__k8s__api__autoscaling__v2beta1__PodsMetricStatus]:
        return self._pods

    @property
    def resource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__ResourceMetricStatus]:
        return self._resource

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        containerResource: Optional[
            io__k8s__api__autoscaling__v2beta1__ContainerResourceMetricStatus
        ] = None,
        external: Optional[
            io__k8s__api__autoscaling__v2beta1__ExternalMetricStatus
        ] = None,
        object: Optional[io__k8s__api__autoscaling__v2beta1__ObjectMetricStatus] = None,
        pods: Optional[io__k8s__api__autoscaling__v2beta1__PodsMetricStatus] = None,
        resource: Optional[
            io__k8s__api__autoscaling__v2beta1__ResourceMetricStatus
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if containerResource is not None:
            self._containerResource = containerResource
        if external is not None:
            self._external = external
        if object is not None:
            self._object = object
        if pods is not None:
            self._pods = pods
        if resource is not None:
            self._resource = resource


class io__k8s__api__autoscaling__v2beta2__ExternalMetricSource(K8STemplatable):
    """ExternalMetricSource indicates how to scale on a metric not associated with any Kubernetes object (for example length of queue in cloud messaging service, or QPS from loadbalancer running outside of cluster)."""

    props: List[str] = ["metric", "target"]
    required_props: List[str] = ["metric", "target"]

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2beta2__MetricIdentifier:
        return self._metric

    @property
    def target(self) -> io__k8s__api__autoscaling__v2beta2__MetricTarget:
        return self._target

    def __init__(
        self,
        metric: io__k8s__api__autoscaling__v2beta2__MetricIdentifier,
        target: io__k8s__api__autoscaling__v2beta2__MetricTarget,
    ):
        super().__init__()
        if metric is not None:
            self._metric = metric
        if target is not None:
            self._target = target


class io__k8s__api__autoscaling__v2beta2__ExternalMetricStatus(K8STemplatable):
    """ExternalMetricStatus indicates the current value of a global metric not associated with any Kubernetes object."""

    props: List[str] = ["current", "metric"]
    required_props: List[str] = ["metric", "current"]

    @property
    def current(self) -> io__k8s__api__autoscaling__v2beta2__MetricValueStatus:
        return self._current

    @property
    def metric(self) -> io__k8s__api__autoscaling__v2beta2__MetricIdentifier:
        return self._metric

    def __init__(
        self,
        current: io__k8s__api__autoscaling__v2beta2__MetricValueStatus,
        metric: io__k8s__api__autoscaling__v2beta2__MetricIdentifier,
    ):
        super().__init__()
        if current is not None:
            self._current = current
        if metric is not None:
            self._metric = metric


class io__k8s__api__autoscaling__v2beta2__MetricSpec(K8STemplatable):
    """MetricSpec specifies how to scale based on a single metric (only `type` and one other matching field should be set at once)."""

    props: List[str] = [
        "containerResource",
        "external",
        "object",
        "pods",
        "resource",
        "type",
    ]
    required_props: List[str] = ["type"]

    @property
    def containerResource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__ContainerResourceMetricSource]:
        return self._containerResource

    @property
    def external(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__ExternalMetricSource]:
        return self._external

    @property
    def object(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__ObjectMetricSource]:
        return self._object

    @property
    def pods(self) -> Optional[io__k8s__api__autoscaling__v2beta2__PodsMetricSource]:
        return self._pods

    @property
    def resource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__ResourceMetricSource]:
        return self._resource

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        containerResource: Optional[
            io__k8s__api__autoscaling__v2beta2__ContainerResourceMetricSource
        ] = None,
        external: Optional[
            io__k8s__api__autoscaling__v2beta2__ExternalMetricSource
        ] = None,
        object: Optional[io__k8s__api__autoscaling__v2beta2__ObjectMetricSource] = None,
        pods: Optional[io__k8s__api__autoscaling__v2beta2__PodsMetricSource] = None,
        resource: Optional[
            io__k8s__api__autoscaling__v2beta2__ResourceMetricSource
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if containerResource is not None:
            self._containerResource = containerResource
        if external is not None:
            self._external = external
        if object is not None:
            self._object = object
        if pods is not None:
            self._pods = pods
        if resource is not None:
            self._resource = resource


class io__k8s__api__autoscaling__v2beta2__MetricStatus(K8STemplatable):
    """MetricStatus describes the last-read state of a single metric."""

    props: List[str] = [
        "containerResource",
        "external",
        "object",
        "pods",
        "resource",
        "type",
    ]
    required_props: List[str] = ["type"]

    @property
    def containerResource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__ContainerResourceMetricStatus]:
        return self._containerResource

    @property
    def external(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__ExternalMetricStatus]:
        return self._external

    @property
    def object(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__ObjectMetricStatus]:
        return self._object

    @property
    def pods(self) -> Optional[io__k8s__api__autoscaling__v2beta2__PodsMetricStatus]:
        return self._pods

    @property
    def resource(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__ResourceMetricStatus]:
        return self._resource

    @property
    def type(self) -> str:
        return self._type

    def __init__(
        self,
        type: str,
        containerResource: Optional[
            io__k8s__api__autoscaling__v2beta2__ContainerResourceMetricStatus
        ] = None,
        external: Optional[
            io__k8s__api__autoscaling__v2beta2__ExternalMetricStatus
        ] = None,
        object: Optional[io__k8s__api__autoscaling__v2beta2__ObjectMetricStatus] = None,
        pods: Optional[io__k8s__api__autoscaling__v2beta2__PodsMetricStatus] = None,
        resource: Optional[
            io__k8s__api__autoscaling__v2beta2__ResourceMetricStatus
        ] = None,
    ):
        super().__init__()
        if type is not None:
            self._type = type
        if containerResource is not None:
            self._containerResource = containerResource
        if external is not None:
            self._external = external
        if object is not None:
            self._object = object
        if pods is not None:
            self._pods = pods
        if resource is not None:
            self._resource = resource


class io__k8s__api__core__v1__DownwardAPIProjection(K8STemplatable):
    """Represents downward API info for projecting into a projected volume. Note that this is identical to a downwardAPI volume source without the default mode."""

    props: List[str] = ["items"]
    required_props: List[str] = []

    @property
    def items(self) -> Optional[List[io__k8s__api__core__v1__DownwardAPIVolumeFile]]:
        return self._items

    def __init__(
        self,
        items: Optional[List[io__k8s__api__core__v1__DownwardAPIVolumeFile]] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items


class io__k8s__api__core__v1__EnvVar(K8STemplatable):
    """EnvVar represents an environment variable present in a Container."""

    props: List[str] = ["name", "value", "valueFrom"]
    required_props: List[str] = ["name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Optional[str]:
        return self._value

    @property
    def valueFrom(self) -> Optional[io__k8s__api__core__v1__EnvVarSource]:
        return self._valueFrom

    def __init__(
        self,
        name: str,
        value: Optional[str] = None,
        valueFrom: Optional[io__k8s__api__core__v1__EnvVarSource] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if value is not None:
            self._value = value
        if valueFrom is not None:
            self._valueFrom = valueFrom


class io__k8s__api__core__v1__EphemeralVolumeSource(K8STemplatable):
    """Represents an ephemeral volume that is handled by a normal storage driver."""

    props: List[str] = ["volumeClaimTemplate"]
    required_props: List[str] = []

    @property
    def volumeClaimTemplate(
        self,
    ) -> Optional[io__k8s__api__core__v1__PersistentVolumeClaimTemplate]:
        return self._volumeClaimTemplate

    def __init__(
        self,
        volumeClaimTemplate: Optional[
            io__k8s__api__core__v1__PersistentVolumeClaimTemplate
        ] = None,
    ):
        super().__init__()
        if volumeClaimTemplate is not None:
            self._volumeClaimTemplate = volumeClaimTemplate


class io__k8s__api__core__v1__Lifecycle(K8STemplatable):
    """Lifecycle describes actions that the management system should take in response to container lifecycle events. For the PostStart and PreStop lifecycle handlers, management of the container blocks until the action is complete, unless the container process fails, in which case the handler is aborted."""

    props: List[str] = ["postStart", "preStop"]
    required_props: List[str] = []

    @property
    def postStart(self) -> Optional[io__k8s__api__core__v1__LifecycleHandler]:
        return self._postStart

    @property
    def preStop(self) -> Optional[io__k8s__api__core__v1__LifecycleHandler]:
        return self._preStop

    def __init__(
        self,
        postStart: Optional[io__k8s__api__core__v1__LifecycleHandler] = None,
        preStop: Optional[io__k8s__api__core__v1__LifecycleHandler] = None,
    ):
        super().__init__()
        if postStart is not None:
            self._postStart = postStart
        if preStop is not None:
            self._preStop = preStop


class io__k8s__api__core__v1__Node(K8STemplatable):
    """Node is a worker node in Kubernetes. Each node will have a unique identifier in the cache (i.e. in etcd)."""

    apiVersion: str = "v1"
    kind: str = "Node"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__NodeSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__core__v1__NodeStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__NodeSpec] = None,
        status: Optional[io__k8s__api__core__v1__NodeStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__core__v1__NodeList(K8STemplatable):
    """NodeList is the whole list of all Nodes which have been registered with master."""

    apiVersion: str = "v1"
    kind: str = "NodeList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__Node]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__Node],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__PersistentVolume(K8STemplatable):
    """PersistentVolume (PV) is a storage resource provisioned by an administrator. It is analogous to a node. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes"""

    apiVersion: str = "v1"
    kind: str = "PersistentVolume"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__PersistentVolumeSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__core__v1__PersistentVolumeStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__PersistentVolumeSpec] = None,
        status: Optional[io__k8s__api__core__v1__PersistentVolumeStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__core__v1__PersistentVolumeClaim(K8STemplatable):
    """PersistentVolumeClaim is a user's request for and claim to a persistent volume"""

    apiVersion: str = "v1"
    kind: str = "PersistentVolumeClaim"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__PersistentVolumeClaimSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__core__v1__PersistentVolumeClaimStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__PersistentVolumeClaimSpec] = None,
        status: Optional[io__k8s__api__core__v1__PersistentVolumeClaimStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__core__v1__PersistentVolumeClaimList(K8STemplatable):
    """PersistentVolumeClaimList is a list of PersistentVolumeClaim items."""

    apiVersion: str = "v1"
    kind: str = "PersistentVolumeClaimList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__PersistentVolumeClaim]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__PersistentVolumeClaim],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__PersistentVolumeList(K8STemplatable):
    """PersistentVolumeList is a list of PersistentVolume items."""

    apiVersion: str = "v1"
    kind: str = "PersistentVolumeList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__PersistentVolume]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__PersistentVolume],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__PodAffinity(K8STemplatable):
    """Pod affinity is a group of inter pod affinity scheduling rules."""

    props: List[str] = [
        "preferredDuringSchedulingIgnoredDuringExecution",
        "requiredDuringSchedulingIgnoredDuringExecution",
    ]
    required_props: List[str] = []

    @property
    def preferredDuringSchedulingIgnoredDuringExecution(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__WeightedPodAffinityTerm]]:
        return self._preferredDuringSchedulingIgnoredDuringExecution

    @property
    def requiredDuringSchedulingIgnoredDuringExecution(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__PodAffinityTerm]]:
        return self._requiredDuringSchedulingIgnoredDuringExecution

    def __init__(
        self,
        preferredDuringSchedulingIgnoredDuringExecution: Optional[
            List[io__k8s__api__core__v1__WeightedPodAffinityTerm]
        ] = None,
        requiredDuringSchedulingIgnoredDuringExecution: Optional[
            List[io__k8s__api__core__v1__PodAffinityTerm]
        ] = None,
    ):
        super().__init__()
        if preferredDuringSchedulingIgnoredDuringExecution is not None:
            self._preferredDuringSchedulingIgnoredDuringExecution = (
                preferredDuringSchedulingIgnoredDuringExecution
            )
        if requiredDuringSchedulingIgnoredDuringExecution is not None:
            self._requiredDuringSchedulingIgnoredDuringExecution = (
                requiredDuringSchedulingIgnoredDuringExecution
            )


class io__k8s__api__core__v1__PodAntiAffinity(K8STemplatable):
    """Pod anti affinity is a group of inter pod anti affinity scheduling rules."""

    props: List[str] = [
        "preferredDuringSchedulingIgnoredDuringExecution",
        "requiredDuringSchedulingIgnoredDuringExecution",
    ]
    required_props: List[str] = []

    @property
    def preferredDuringSchedulingIgnoredDuringExecution(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__WeightedPodAffinityTerm]]:
        return self._preferredDuringSchedulingIgnoredDuringExecution

    @property
    def requiredDuringSchedulingIgnoredDuringExecution(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__PodAffinityTerm]]:
        return self._requiredDuringSchedulingIgnoredDuringExecution

    def __init__(
        self,
        preferredDuringSchedulingIgnoredDuringExecution: Optional[
            List[io__k8s__api__core__v1__WeightedPodAffinityTerm]
        ] = None,
        requiredDuringSchedulingIgnoredDuringExecution: Optional[
            List[io__k8s__api__core__v1__PodAffinityTerm]
        ] = None,
    ):
        super().__init__()
        if preferredDuringSchedulingIgnoredDuringExecution is not None:
            self._preferredDuringSchedulingIgnoredDuringExecution = (
                preferredDuringSchedulingIgnoredDuringExecution
            )
        if requiredDuringSchedulingIgnoredDuringExecution is not None:
            self._requiredDuringSchedulingIgnoredDuringExecution = (
                requiredDuringSchedulingIgnoredDuringExecution
            )


class io__k8s__api__core__v1__ResourceQuota(K8STemplatable):
    """ResourceQuota sets aggregate quota restrictions enforced per namespace"""

    apiVersion: str = "v1"
    kind: str = "ResourceQuota"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__ResourceQuotaSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__core__v1__ResourceQuotaStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__ResourceQuotaSpec] = None,
        status: Optional[io__k8s__api__core__v1__ResourceQuotaStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__core__v1__ResourceQuotaList(K8STemplatable):
    """ResourceQuotaList is a list of ResourceQuota items."""

    apiVersion: str = "v1"
    kind: str = "ResourceQuotaList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__ResourceQuota]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__ResourceQuota],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__Service(K8STemplatable):
    """Service is a named abstraction of software service (for example, mysql) consisting of local port (for example 3306) that the proxy listens on, and the selector that determines which pods will answer requests sent through the proxy."""

    apiVersion: str = "v1"
    kind: str = "Service"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__ServiceSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__core__v1__ServiceStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__ServiceSpec] = None,
        status: Optional[io__k8s__api__core__v1__ServiceStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__core__v1__ServiceList(K8STemplatable):
    """ServiceList holds a list of services."""

    apiVersion: str = "v1"
    kind: str = "ServiceList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__Service]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__Service],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__VolumeProjection(K8STemplatable):
    """Projection that may be projected along with other supported volume types"""

    props: List[str] = ["configMap", "downwardAPI", "secret", "serviceAccountToken"]
    required_props: List[str] = []

    @property
    def configMap(self) -> Optional[io__k8s__api__core__v1__ConfigMapProjection]:
        return self._configMap

    @property
    def downwardAPI(self) -> Optional[io__k8s__api__core__v1__DownwardAPIProjection]:
        return self._downwardAPI

    @property
    def secret(self) -> Optional[io__k8s__api__core__v1__SecretProjection]:
        return self._secret

    @property
    def serviceAccountToken(
        self,
    ) -> Optional[io__k8s__api__core__v1__ServiceAccountTokenProjection]:
        return self._serviceAccountToken

    def __init__(
        self,
        configMap: Optional[io__k8s__api__core__v1__ConfigMapProjection] = None,
        downwardAPI: Optional[io__k8s__api__core__v1__DownwardAPIProjection] = None,
        secret: Optional[io__k8s__api__core__v1__SecretProjection] = None,
        serviceAccountToken: Optional[
            io__k8s__api__core__v1__ServiceAccountTokenProjection
        ] = None,
    ):
        super().__init__()
        if configMap is not None:
            self._configMap = configMap
        if downwardAPI is not None:
            self._downwardAPI = downwardAPI
        if secret is not None:
            self._secret = secret
        if serviceAccountToken is not None:
            self._serviceAccountToken = serviceAccountToken


class io__k8s__api__flowcontrol__v1beta1__FlowSchemaSpec(K8STemplatable):
    """FlowSchemaSpec describes how the FlowSchema's specification looks like."""

    props: List[str] = [
        "distinguisherMethod",
        "matchingPrecedence",
        "priorityLevelConfiguration",
        "rules",
    ]
    required_props: List[str] = ["priorityLevelConfiguration"]

    @property
    def distinguisherMethod(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta1__FlowDistinguisherMethod]:
        return self._distinguisherMethod

    @property
    def matchingPrecedence(self) -> Optional[int]:
        return self._matchingPrecedence

    @property
    def priorityLevelConfiguration(
        self,
    ) -> io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationReference:
        return self._priorityLevelConfiguration

    @property
    def rules(
        self,
    ) -> Optional[List[io__k8s__api__flowcontrol__v1beta1__PolicyRulesWithSubjects]]:
        return self._rules

    def __init__(
        self,
        priorityLevelConfiguration: io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationReference,
        distinguisherMethod: Optional[
            io__k8s__api__flowcontrol__v1beta1__FlowDistinguisherMethod
        ] = None,
        matchingPrecedence: Optional[int] = None,
        rules: Optional[
            List[io__k8s__api__flowcontrol__v1beta1__PolicyRulesWithSubjects]
        ] = None,
    ):
        super().__init__()
        if priorityLevelConfiguration is not None:
            self._priorityLevelConfiguration = priorityLevelConfiguration
        if distinguisherMethod is not None:
            self._distinguisherMethod = distinguisherMethod
        if matchingPrecedence is not None:
            self._matchingPrecedence = matchingPrecedence
        if rules is not None:
            self._rules = rules


class io__k8s__api__flowcontrol__v1beta2__FlowSchemaSpec(K8STemplatable):
    """FlowSchemaSpec describes how the FlowSchema's specification looks like."""

    props: List[str] = [
        "distinguisherMethod",
        "matchingPrecedence",
        "priorityLevelConfiguration",
        "rules",
    ]
    required_props: List[str] = ["priorityLevelConfiguration"]

    @property
    def distinguisherMethod(
        self,
    ) -> Optional[io__k8s__api__flowcontrol__v1beta2__FlowDistinguisherMethod]:
        return self._distinguisherMethod

    @property
    def matchingPrecedence(self) -> Optional[int]:
        return self._matchingPrecedence

    @property
    def priorityLevelConfiguration(
        self,
    ) -> io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationReference:
        return self._priorityLevelConfiguration

    @property
    def rules(
        self,
    ) -> Optional[List[io__k8s__api__flowcontrol__v1beta2__PolicyRulesWithSubjects]]:
        return self._rules

    def __init__(
        self,
        priorityLevelConfiguration: io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationReference,
        distinguisherMethod: Optional[
            io__k8s__api__flowcontrol__v1beta2__FlowDistinguisherMethod
        ] = None,
        matchingPrecedence: Optional[int] = None,
        rules: Optional[
            List[io__k8s__api__flowcontrol__v1beta2__PolicyRulesWithSubjects]
        ] = None,
    ):
        super().__init__()
        if priorityLevelConfiguration is not None:
            self._priorityLevelConfiguration = priorityLevelConfiguration
        if distinguisherMethod is not None:
            self._distinguisherMethod = distinguisherMethod
        if matchingPrecedence is not None:
            self._matchingPrecedence = matchingPrecedence
        if rules is not None:
            self._rules = rules


class io__k8s__api__networking__v1__HTTPIngressPath(K8STemplatable):
    """HTTPIngressPath associates a path with a backend. Incoming urls matching the path are forwarded to the backend."""

    props: List[str] = ["backend", "path", "pathType"]
    required_props: List[str] = ["pathType", "backend"]

    @property
    def backend(self) -> io__k8s__api__networking__v1__IngressBackend:
        return self._backend

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def pathType(self) -> str:
        return self._pathType

    def __init__(
        self,
        backend: io__k8s__api__networking__v1__IngressBackend,
        pathType: str,
        path: Optional[str] = None,
    ):
        super().__init__()
        if backend is not None:
            self._backend = backend
        if pathType is not None:
            self._pathType = pathType
        if path is not None:
            self._path = path


class io__k8s__api__networking__v1__HTTPIngressRuleValue(K8STemplatable):
    """HTTPIngressRuleValue is a list of http selectors pointing to backends. In the example: http://<host>/<path>?<searchpart> -> backend where where parts of the url correspond to RFC 3986, this resource will be used to match against everything after the last '/' and before the first '?' or '#'."""

    props: List[str] = ["paths"]
    required_props: List[str] = ["paths"]

    @property
    def paths(self) -> List[io__k8s__api__networking__v1__HTTPIngressPath]:
        return self._paths

    def __init__(self, paths: List[io__k8s__api__networking__v1__HTTPIngressPath]):
        super().__init__()
        if paths is not None:
            self._paths = paths


class io__k8s__api__networking__v1__IngressRule(K8STemplatable):
    """IngressRule represents the rules mapping the paths under a specified host to the related backend services. Incoming requests are first evaluated for a host match, then routed to the backend associated with the matching IngressRuleValue."""

    props: List[str] = ["host", "http"]
    required_props: List[str] = []

    @property
    def host(self) -> Optional[str]:
        return self._host

    @property
    def http(self) -> Optional[io__k8s__api__networking__v1__HTTPIngressRuleValue]:
        return self._http

    def __init__(
        self,
        host: Optional[str] = None,
        http: Optional[io__k8s__api__networking__v1__HTTPIngressRuleValue] = None,
    ):
        super().__init__()
        if host is not None:
            self._host = host
        if http is not None:
            self._http = http


class io__k8s__api__networking__v1__IngressSpec(K8STemplatable):
    """IngressSpec describes the Ingress the user wishes to exist."""

    props: List[str] = ["defaultBackend", "ingressClassName", "rules", "tls"]
    required_props: List[str] = []

    @property
    def defaultBackend(self) -> Optional[io__k8s__api__networking__v1__IngressBackend]:
        return self._defaultBackend

    @property
    def ingressClassName(self) -> Optional[str]:
        return self._ingressClassName

    @property
    def rules(self) -> Optional[List[io__k8s__api__networking__v1__IngressRule]]:
        return self._rules

    @property
    def tls(self) -> Optional[List[io__k8s__api__networking__v1__IngressTLS]]:
        return self._tls

    def __init__(
        self,
        defaultBackend: Optional[io__k8s__api__networking__v1__IngressBackend] = None,
        ingressClassName: Optional[str] = None,
        rules: Optional[List[io__k8s__api__networking__v1__IngressRule]] = None,
        tls: Optional[List[io__k8s__api__networking__v1__IngressTLS]] = None,
    ):
        super().__init__()
        if defaultBackend is not None:
            self._defaultBackend = defaultBackend
        if ingressClassName is not None:
            self._ingressClassName = ingressClassName
        if rules is not None:
            self._rules = rules
        if tls is not None:
            self._tls = tls


class io__k8s__api__networking__v1__NetworkPolicyEgressRule(K8STemplatable):
    """NetworkPolicyEgressRule describes a particular set of traffic that is allowed out of pods matched by a NetworkPolicySpec's podSelector. The traffic must match both ports and to. This type is beta-level in 1.8"""

    props: List[str] = ["ports", "to"]
    required_props: List[str] = []

    @property
    def ports(self) -> Optional[List[io__k8s__api__networking__v1__NetworkPolicyPort]]:
        return self._ports

    @property
    def to(self) -> Optional[List[io__k8s__api__networking__v1__NetworkPolicyPeer]]:
        return self._to

    def __init__(
        self,
        ports: Optional[List[io__k8s__api__networking__v1__NetworkPolicyPort]] = None,
        to: Optional[List[io__k8s__api__networking__v1__NetworkPolicyPeer]] = None,
    ):
        super().__init__()
        if ports is not None:
            self._ports = ports
        if to is not None:
            self._to = to


class io__k8s__api__networking__v1__NetworkPolicyIngressRule(K8STemplatable):
    """NetworkPolicyIngressRule describes a particular set of traffic that is allowed to the pods matched by a NetworkPolicySpec's podSelector. The traffic must match both ports and from."""

    props: List[str] = ["k8s_from", "ports"]
    required_props: List[str] = []

    @property
    def k8s_from(
        self,
    ) -> Optional[List[io__k8s__api__networking__v1__NetworkPolicyPeer]]:
        return self._k8s_from

    @property
    def ports(self) -> Optional[List[io__k8s__api__networking__v1__NetworkPolicyPort]]:
        return self._ports

    def __init__(
        self,
        k8s_from: Optional[
            List[io__k8s__api__networking__v1__NetworkPolicyPeer]
        ] = None,
        ports: Optional[List[io__k8s__api__networking__v1__NetworkPolicyPort]] = None,
    ):
        super().__init__()
        if k8s_from is not None:
            self._k8s_from = k8s_from
        if ports is not None:
            self._ports = ports


class io__k8s__api__networking__v1__NetworkPolicySpec(K8STemplatable):
    """NetworkPolicySpec provides the specification of a NetworkPolicy"""

    props: List[str] = ["egress", "ingress", "podSelector", "policyTypes"]
    required_props: List[str] = ["podSelector"]

    @property
    def egress(
        self,
    ) -> Optional[List[io__k8s__api__networking__v1__NetworkPolicyEgressRule]]:
        return self._egress

    @property
    def ingress(
        self,
    ) -> Optional[List[io__k8s__api__networking__v1__NetworkPolicyIngressRule]]:
        return self._ingress

    @property
    def podSelector(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector:
        return self._podSelector

    @property
    def policyTypes(self) -> Optional[List[str]]:
        return self._policyTypes

    def __init__(
        self,
        podSelector: io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector,
        egress: Optional[
            List[io__k8s__api__networking__v1__NetworkPolicyEgressRule]
        ] = None,
        ingress: Optional[
            List[io__k8s__api__networking__v1__NetworkPolicyIngressRule]
        ] = None,
        policyTypes: Optional[List[str]] = None,
    ):
        super().__init__()
        if podSelector is not None:
            self._podSelector = podSelector
        if egress is not None:
            self._egress = egress
        if ingress is not None:
            self._ingress = ingress
        if policyTypes is not None:
            self._policyTypes = policyTypes


class io__k8s__api__policy__v1__PodDisruptionBudget(K8STemplatable):
    """PodDisruptionBudget is an object to define the max disruption that can be caused to a collection of pods"""

    apiVersion: str = "policy/v1"
    kind: str = "PodDisruptionBudget"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__policy__v1__PodDisruptionBudgetSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__policy__v1__PodDisruptionBudgetStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__policy__v1__PodDisruptionBudgetSpec] = None,
        status: Optional[io__k8s__api__policy__v1__PodDisruptionBudgetStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__policy__v1__PodDisruptionBudgetList(K8STemplatable):
    """PodDisruptionBudgetList is a collection of PodDisruptionBudgets."""

    apiVersion: str = "policy/v1"
    kind: str = "PodDisruptionBudgetList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__policy__v1__PodDisruptionBudget]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__policy__v1__PodDisruptionBudget],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__policy__v1beta1__PodDisruptionBudget(K8STemplatable):
    """PodDisruptionBudget is an object to define the max disruption that can be caused to a collection of pods"""

    apiVersion: str = "policy/v1beta1"
    kind: str = "PodDisruptionBudget"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__policy__v1beta1__PodDisruptionBudgetSpec]:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__policy__v1beta1__PodDisruptionBudgetStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__policy__v1beta1__PodDisruptionBudgetSpec] = None,
        status: Optional[
            io__k8s__api__policy__v1beta1__PodDisruptionBudgetStatus
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__policy__v1beta1__PodDisruptionBudgetList(K8STemplatable):
    """PodDisruptionBudgetList is a collection of PodDisruptionBudgets."""

    apiVersion: str = "policy/v1beta1"
    kind: str = "PodDisruptionBudgetList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__policy__v1beta1__PodDisruptionBudget]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__policy__v1beta1__PodDisruptionBudget],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__storage__v1__VolumeAttachment(K8STemplatable):
    """VolumeAttachment captures the intent to attach or detach the specified volume to/from the specified node.

    VolumeAttachment objects are non-namespaced."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "VolumeAttachment"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> io__k8s__api__storage__v1__VolumeAttachmentSpec:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__storage__v1__VolumeAttachmentStatus]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__api__storage__v1__VolumeAttachmentSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[io__k8s__api__storage__v1__VolumeAttachmentStatus] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__api__storage__v1__VolumeAttachmentList(K8STemplatable):
    """VolumeAttachmentList is a collection of VolumeAttachment objects."""

    apiVersion: str = "storage.k8s.io/v1"
    kind: str = "VolumeAttachmentList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__storage__v1__VolumeAttachment]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__storage__v1__VolumeAttachment],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionVersion(
    K8STemplatable
):
    """CustomResourceDefinitionVersion describes a version for CRD."""

    props: List[str] = [
        "additionalPrinterColumns",
        "deprecated",
        "deprecationWarning",
        "name",
        "schema",
        "served",
        "storage",
        "subresources",
    ]
    required_props: List[str] = ["name", "served", "storage"]

    @property
    def additionalPrinterColumns(
        self,
    ) -> Optional[
        List[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceColumnDefinition
        ]
    ]:
        return self._additionalPrinterColumns

    @property
    def deprecated(self) -> Optional[bool]:
        return self._deprecated

    @property
    def deprecationWarning(self) -> Optional[str]:
        return self._deprecationWarning

    @property
    def name(self) -> str:
        return self._name

    @property
    def schema(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceValidation
    ]:
        return self._schema

    @property
    def served(self) -> bool:
        return self._served

    @property
    def storage(self) -> bool:
        return self._storage

    @property
    def subresources(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresources
    ]:
        return self._subresources

    def __init__(
        self,
        name: str,
        served: bool,
        storage: bool,
        additionalPrinterColumns: Optional[
            List[
                io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceColumnDefinition
            ]
        ] = None,
        deprecated: Optional[bool] = None,
        deprecationWarning: Optional[str] = None,
        schema: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceValidation
        ] = None,
        subresources: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresources
        ] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if served is not None:
            self._served = served
        if storage is not None:
            self._storage = storage
        if additionalPrinterColumns is not None:
            self._additionalPrinterColumns = additionalPrinterColumns
        if deprecated is not None:
            self._deprecated = deprecated
        if deprecationWarning is not None:
            self._deprecationWarning = deprecationWarning
        if schema is not None:
            self._schema = schema
        if subresources is not None:
            self._subresources = subresources


class io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerSpec(K8STemplatable):
    """HorizontalPodAutoscalerSpec describes the desired functionality of the HorizontalPodAutoscaler."""

    props: List[str] = [
        "behavior",
        "maxReplicas",
        "metrics",
        "minReplicas",
        "scaleTargetRef",
    ]
    required_props: List[str] = ["scaleTargetRef", "maxReplicas"]

    @property
    def behavior(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerBehavior]:
        return self._behavior

    @property
    def maxReplicas(self) -> int:
        return self._maxReplicas

    @property
    def metrics(self) -> Optional[List[io__k8s__api__autoscaling__v2__MetricSpec]]:
        return self._metrics

    @property
    def minReplicas(self) -> Optional[int]:
        return self._minReplicas

    @property
    def scaleTargetRef(
        self,
    ) -> io__k8s__api__autoscaling__v2__CrossVersionObjectReference:
        return self._scaleTargetRef

    def __init__(
        self,
        maxReplicas: int,
        scaleTargetRef: io__k8s__api__autoscaling__v2__CrossVersionObjectReference,
        behavior: Optional[
            io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerBehavior
        ] = None,
        metrics: Optional[List[io__k8s__api__autoscaling__v2__MetricSpec]] = None,
        minReplicas: Optional[int] = None,
    ):
        super().__init__()
        if maxReplicas is not None:
            self._maxReplicas = maxReplicas
        if scaleTargetRef is not None:
            self._scaleTargetRef = scaleTargetRef
        if behavior is not None:
            self._behavior = behavior
        if metrics is not None:
            self._metrics = metrics
        if minReplicas is not None:
            self._minReplicas = minReplicas


class io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerStatus(K8STemplatable):
    """HorizontalPodAutoscalerStatus describes the current status of a horizontal pod autoscaler."""

    props: List[str] = [
        "conditions",
        "currentMetrics",
        "currentReplicas",
        "desiredReplicas",
        "lastScaleTime",
        "observedGeneration",
    ]
    required_props: List[str] = ["desiredReplicas"]

    @property
    def conditions(
        self,
    ) -> Optional[
        List[io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerCondition]
    ]:
        return self._conditions

    @property
    def currentMetrics(
        self,
    ) -> Optional[List[io__k8s__api__autoscaling__v2__MetricStatus]]:
        return self._currentMetrics

    @property
    def currentReplicas(self) -> Optional[int]:
        return self._currentReplicas

    @property
    def desiredReplicas(self) -> int:
        return self._desiredReplicas

    @property
    def lastScaleTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastScaleTime

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    def __init__(
        self,
        desiredReplicas: int,
        conditions: Optional[
            List[io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerCondition]
        ] = None,
        currentMetrics: Optional[
            List[io__k8s__api__autoscaling__v2__MetricStatus]
        ] = None,
        currentReplicas: Optional[int] = None,
        lastScaleTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        observedGeneration: Optional[int] = None,
    ):
        super().__init__()
        if desiredReplicas is not None:
            self._desiredReplicas = desiredReplicas
        if conditions is not None:
            self._conditions = conditions
        if currentMetrics is not None:
            self._currentMetrics = currentMetrics
        if currentReplicas is not None:
            self._currentReplicas = currentReplicas
        if lastScaleTime is not None:
            self._lastScaleTime = lastScaleTime
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration


class io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerSpec(K8STemplatable):
    """HorizontalPodAutoscalerSpec describes the desired functionality of the HorizontalPodAutoscaler."""

    props: List[str] = ["maxReplicas", "metrics", "minReplicas", "scaleTargetRef"]
    required_props: List[str] = ["scaleTargetRef", "maxReplicas"]

    @property
    def maxReplicas(self) -> int:
        return self._maxReplicas

    @property
    def metrics(self) -> Optional[List[io__k8s__api__autoscaling__v2beta1__MetricSpec]]:
        return self._metrics

    @property
    def minReplicas(self) -> Optional[int]:
        return self._minReplicas

    @property
    def scaleTargetRef(
        self,
    ) -> io__k8s__api__autoscaling__v2beta1__CrossVersionObjectReference:
        return self._scaleTargetRef

    def __init__(
        self,
        maxReplicas: int,
        scaleTargetRef: io__k8s__api__autoscaling__v2beta1__CrossVersionObjectReference,
        metrics: Optional[List[io__k8s__api__autoscaling__v2beta1__MetricSpec]] = None,
        minReplicas: Optional[int] = None,
    ):
        super().__init__()
        if maxReplicas is not None:
            self._maxReplicas = maxReplicas
        if scaleTargetRef is not None:
            self._scaleTargetRef = scaleTargetRef
        if metrics is not None:
            self._metrics = metrics
        if minReplicas is not None:
            self._minReplicas = minReplicas


class io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerStatus(K8STemplatable):
    """HorizontalPodAutoscalerStatus describes the current status of a horizontal pod autoscaler."""

    props: List[str] = [
        "conditions",
        "currentMetrics",
        "currentReplicas",
        "desiredReplicas",
        "lastScaleTime",
        "observedGeneration",
    ]
    required_props: List[str] = ["currentReplicas", "desiredReplicas"]

    @property
    def conditions(
        self,
    ) -> Optional[
        List[io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerCondition]
    ]:
        return self._conditions

    @property
    def currentMetrics(
        self,
    ) -> Optional[List[io__k8s__api__autoscaling__v2beta1__MetricStatus]]:
        return self._currentMetrics

    @property
    def currentReplicas(self) -> int:
        return self._currentReplicas

    @property
    def desiredReplicas(self) -> int:
        return self._desiredReplicas

    @property
    def lastScaleTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastScaleTime

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    def __init__(
        self,
        currentReplicas: int,
        desiredReplicas: int,
        conditions: Optional[
            List[io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerCondition]
        ] = None,
        currentMetrics: Optional[
            List[io__k8s__api__autoscaling__v2beta1__MetricStatus]
        ] = None,
        lastScaleTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        observedGeneration: Optional[int] = None,
    ):
        super().__init__()
        if currentReplicas is not None:
            self._currentReplicas = currentReplicas
        if desiredReplicas is not None:
            self._desiredReplicas = desiredReplicas
        if conditions is not None:
            self._conditions = conditions
        if currentMetrics is not None:
            self._currentMetrics = currentMetrics
        if lastScaleTime is not None:
            self._lastScaleTime = lastScaleTime
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration


class io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerSpec(K8STemplatable):
    """HorizontalPodAutoscalerSpec describes the desired functionality of the HorizontalPodAutoscaler."""

    props: List[str] = [
        "behavior",
        "maxReplicas",
        "metrics",
        "minReplicas",
        "scaleTargetRef",
    ]
    required_props: List[str] = ["scaleTargetRef", "maxReplicas"]

    @property
    def behavior(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerBehavior]:
        return self._behavior

    @property
    def maxReplicas(self) -> int:
        return self._maxReplicas

    @property
    def metrics(self) -> Optional[List[io__k8s__api__autoscaling__v2beta2__MetricSpec]]:
        return self._metrics

    @property
    def minReplicas(self) -> Optional[int]:
        return self._minReplicas

    @property
    def scaleTargetRef(
        self,
    ) -> io__k8s__api__autoscaling__v2beta2__CrossVersionObjectReference:
        return self._scaleTargetRef

    def __init__(
        self,
        maxReplicas: int,
        scaleTargetRef: io__k8s__api__autoscaling__v2beta2__CrossVersionObjectReference,
        behavior: Optional[
            io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerBehavior
        ] = None,
        metrics: Optional[List[io__k8s__api__autoscaling__v2beta2__MetricSpec]] = None,
        minReplicas: Optional[int] = None,
    ):
        super().__init__()
        if maxReplicas is not None:
            self._maxReplicas = maxReplicas
        if scaleTargetRef is not None:
            self._scaleTargetRef = scaleTargetRef
        if behavior is not None:
            self._behavior = behavior
        if metrics is not None:
            self._metrics = metrics
        if minReplicas is not None:
            self._minReplicas = minReplicas


class io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerStatus(K8STemplatable):
    """HorizontalPodAutoscalerStatus describes the current status of a horizontal pod autoscaler."""

    props: List[str] = [
        "conditions",
        "currentMetrics",
        "currentReplicas",
        "desiredReplicas",
        "lastScaleTime",
        "observedGeneration",
    ]
    required_props: List[str] = ["currentReplicas", "desiredReplicas"]

    @property
    def conditions(
        self,
    ) -> Optional[
        List[io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerCondition]
    ]:
        return self._conditions

    @property
    def currentMetrics(
        self,
    ) -> Optional[List[io__k8s__api__autoscaling__v2beta2__MetricStatus]]:
        return self._currentMetrics

    @property
    def currentReplicas(self) -> int:
        return self._currentReplicas

    @property
    def desiredReplicas(self) -> int:
        return self._desiredReplicas

    @property
    def lastScaleTime(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__Time]:
        return self._lastScaleTime

    @property
    def observedGeneration(self) -> Optional[int]:
        return self._observedGeneration

    def __init__(
        self,
        currentReplicas: int,
        desiredReplicas: int,
        conditions: Optional[
            List[io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerCondition]
        ] = None,
        currentMetrics: Optional[
            List[io__k8s__api__autoscaling__v2beta2__MetricStatus]
        ] = None,
        lastScaleTime: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__Time
        ] = None,
        observedGeneration: Optional[int] = None,
    ):
        super().__init__()
        if currentReplicas is not None:
            self._currentReplicas = currentReplicas
        if desiredReplicas is not None:
            self._desiredReplicas = desiredReplicas
        if conditions is not None:
            self._conditions = conditions
        if currentMetrics is not None:
            self._currentMetrics = currentMetrics
        if lastScaleTime is not None:
            self._lastScaleTime = lastScaleTime
        if observedGeneration is not None:
            self._observedGeneration = observedGeneration


class io__k8s__api__core__v1__Affinity(K8STemplatable):
    """Affinity is a group of affinity scheduling rules."""

    props: List[str] = ["nodeAffinity", "podAffinity", "podAntiAffinity"]
    required_props: List[str] = []

    @property
    def nodeAffinity(self) -> Optional[io__k8s__api__core__v1__NodeAffinity]:
        return self._nodeAffinity

    @property
    def podAffinity(self) -> Optional[io__k8s__api__core__v1__PodAffinity]:
        return self._podAffinity

    @property
    def podAntiAffinity(self) -> Optional[io__k8s__api__core__v1__PodAntiAffinity]:
        return self._podAntiAffinity

    def __init__(
        self,
        nodeAffinity: Optional[io__k8s__api__core__v1__NodeAffinity] = None,
        podAffinity: Optional[io__k8s__api__core__v1__PodAffinity] = None,
        podAntiAffinity: Optional[io__k8s__api__core__v1__PodAntiAffinity] = None,
    ):
        super().__init__()
        if nodeAffinity is not None:
            self._nodeAffinity = nodeAffinity
        if podAffinity is not None:
            self._podAffinity = podAffinity
        if podAntiAffinity is not None:
            self._podAntiAffinity = podAntiAffinity


class io__k8s__api__core__v1__Container(K8STemplatable):
    """A single application container that you want to run within a pod."""

    props: List[str] = [
        "args",
        "command",
        "env",
        "envFrom",
        "image",
        "imagePullPolicy",
        "lifecycle",
        "livenessProbe",
        "name",
        "ports",
        "readinessProbe",
        "resources",
        "securityContext",
        "startupProbe",
        "stdin",
        "stdinOnce",
        "terminationMessagePath",
        "terminationMessagePolicy",
        "tty",
        "volumeDevices",
        "volumeMounts",
        "workingDir",
    ]
    required_props: List[str] = ["name"]

    @property
    def args(self) -> Optional[List[str]]:
        return self._args

    @property
    def command(self) -> Optional[List[str]]:
        return self._command

    @property
    def env(self) -> Optional[List[io__k8s__api__core__v1__EnvVar]]:
        return self._env

    @property
    def envFrom(self) -> Optional[List[io__k8s__api__core__v1__EnvFromSource]]:
        return self._envFrom

    @property
    def image(self) -> Optional[str]:
        return self._image

    @property
    def imagePullPolicy(self) -> Optional[Literal["Always", "IfNotPresent", "Never"]]:
        return self._imagePullPolicy

    @property
    def lifecycle(self) -> Optional[io__k8s__api__core__v1__Lifecycle]:
        return self._lifecycle

    @property
    def livenessProbe(self) -> Optional[io__k8s__api__core__v1__Probe]:
        return self._livenessProbe

    @property
    def name(self) -> str:
        return self._name

    @property
    def ports(self) -> Optional[List[io__k8s__api__core__v1__ContainerPort]]:
        return self._ports

    @property
    def readinessProbe(self) -> Optional[io__k8s__api__core__v1__Probe]:
        return self._readinessProbe

    @property
    def resources(self) -> Optional[io__k8s__api__core__v1__ResourceRequirements]:
        return self._resources

    @property
    def securityContext(self) -> Optional[io__k8s__api__core__v1__SecurityContext]:
        return self._securityContext

    @property
    def startupProbe(self) -> Optional[io__k8s__api__core__v1__Probe]:
        return self._startupProbe

    @property
    def stdin(self) -> Optional[bool]:
        return self._stdin

    @property
    def stdinOnce(self) -> Optional[bool]:
        return self._stdinOnce

    @property
    def terminationMessagePath(self) -> Optional[str]:
        return self._terminationMessagePath

    @property
    def terminationMessagePolicy(
        self,
    ) -> Optional[Literal["FallbackToLogsOnError", "File"]]:
        return self._terminationMessagePolicy

    @property
    def tty(self) -> Optional[bool]:
        return self._tty

    @property
    def volumeDevices(self) -> Optional[List[io__k8s__api__core__v1__VolumeDevice]]:
        return self._volumeDevices

    @property
    def volumeMounts(self) -> Optional[List[io__k8s__api__core__v1__VolumeMount]]:
        return self._volumeMounts

    @property
    def workingDir(self) -> Optional[str]:
        return self._workingDir

    def __init__(
        self,
        name: str,
        args: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        env: Optional[List[io__k8s__api__core__v1__EnvVar]] = None,
        envFrom: Optional[List[io__k8s__api__core__v1__EnvFromSource]] = None,
        image: Optional[str] = None,
        imagePullPolicy: Optional[Literal["Always", "IfNotPresent", "Never"]] = None,
        lifecycle: Optional[io__k8s__api__core__v1__Lifecycle] = None,
        livenessProbe: Optional[io__k8s__api__core__v1__Probe] = None,
        ports: Optional[List[io__k8s__api__core__v1__ContainerPort]] = None,
        readinessProbe: Optional[io__k8s__api__core__v1__Probe] = None,
        resources: Optional[io__k8s__api__core__v1__ResourceRequirements] = None,
        securityContext: Optional[io__k8s__api__core__v1__SecurityContext] = None,
        startupProbe: Optional[io__k8s__api__core__v1__Probe] = None,
        stdin: Optional[bool] = None,
        stdinOnce: Optional[bool] = None,
        terminationMessagePath: Optional[str] = None,
        terminationMessagePolicy: Optional[
            Literal["FallbackToLogsOnError", "File"]
        ] = None,
        tty: Optional[bool] = None,
        volumeDevices: Optional[List[io__k8s__api__core__v1__VolumeDevice]] = None,
        volumeMounts: Optional[List[io__k8s__api__core__v1__VolumeMount]] = None,
        workingDir: Optional[str] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if args is not None:
            self._args = args
        if command is not None:
            self._command = command
        if env is not None:
            self._env = env
        if envFrom is not None:
            self._envFrom = envFrom
        if image is not None:
            self._image = image
        if imagePullPolicy is not None:
            self._imagePullPolicy = imagePullPolicy
        if lifecycle is not None:
            self._lifecycle = lifecycle
        if livenessProbe is not None:
            self._livenessProbe = livenessProbe
        if ports is not None:
            self._ports = ports
        if readinessProbe is not None:
            self._readinessProbe = readinessProbe
        if resources is not None:
            self._resources = resources
        if securityContext is not None:
            self._securityContext = securityContext
        if startupProbe is not None:
            self._startupProbe = startupProbe
        if stdin is not None:
            self._stdin = stdin
        if stdinOnce is not None:
            self._stdinOnce = stdinOnce
        if terminationMessagePath is not None:
            self._terminationMessagePath = terminationMessagePath
        if terminationMessagePolicy is not None:
            self._terminationMessagePolicy = terminationMessagePolicy
        if tty is not None:
            self._tty = tty
        if volumeDevices is not None:
            self._volumeDevices = volumeDevices
        if volumeMounts is not None:
            self._volumeMounts = volumeMounts
        if workingDir is not None:
            self._workingDir = workingDir


class io__k8s__api__core__v1__EphemeralContainer(K8STemplatable):
    """An EphemeralContainer is a temporary container that you may add to an existing Pod for user-initiated activities such as debugging. Ephemeral containers have no resource or scheduling guarantees, and they will not be restarted when they exit or when a Pod is removed or restarted. The kubelet may evict a Pod if an ephemeral container causes the Pod to exceed its resource allocation.

    To add an ephemeral container, use the ephemeralcontainers subresource of an existing Pod. Ephemeral containers may not be removed or restarted.

    This is a beta feature available on clusters that haven't disabled the EphemeralContainers feature gate."""

    props: List[str] = [
        "args",
        "command",
        "env",
        "envFrom",
        "image",
        "imagePullPolicy",
        "lifecycle",
        "livenessProbe",
        "name",
        "ports",
        "readinessProbe",
        "resources",
        "securityContext",
        "startupProbe",
        "stdin",
        "stdinOnce",
        "targetContainerName",
        "terminationMessagePath",
        "terminationMessagePolicy",
        "tty",
        "volumeDevices",
        "volumeMounts",
        "workingDir",
    ]
    required_props: List[str] = ["name"]

    @property
    def args(self) -> Optional[List[str]]:
        return self._args

    @property
    def command(self) -> Optional[List[str]]:
        return self._command

    @property
    def env(self) -> Optional[List[io__k8s__api__core__v1__EnvVar]]:
        return self._env

    @property
    def envFrom(self) -> Optional[List[io__k8s__api__core__v1__EnvFromSource]]:
        return self._envFrom

    @property
    def image(self) -> Optional[str]:
        return self._image

    @property
    def imagePullPolicy(self) -> Optional[Literal["Always", "IfNotPresent", "Never"]]:
        return self._imagePullPolicy

    @property
    def lifecycle(self) -> Optional[io__k8s__api__core__v1__Lifecycle]:
        return self._lifecycle

    @property
    def livenessProbe(self) -> Optional[io__k8s__api__core__v1__Probe]:
        return self._livenessProbe

    @property
    def name(self) -> str:
        return self._name

    @property
    def ports(self) -> Optional[List[io__k8s__api__core__v1__ContainerPort]]:
        return self._ports

    @property
    def readinessProbe(self) -> Optional[io__k8s__api__core__v1__Probe]:
        return self._readinessProbe

    @property
    def resources(self) -> Optional[io__k8s__api__core__v1__ResourceRequirements]:
        return self._resources

    @property
    def securityContext(self) -> Optional[io__k8s__api__core__v1__SecurityContext]:
        return self._securityContext

    @property
    def startupProbe(self) -> Optional[io__k8s__api__core__v1__Probe]:
        return self._startupProbe

    @property
    def stdin(self) -> Optional[bool]:
        return self._stdin

    @property
    def stdinOnce(self) -> Optional[bool]:
        return self._stdinOnce

    @property
    def targetContainerName(self) -> Optional[str]:
        return self._targetContainerName

    @property
    def terminationMessagePath(self) -> Optional[str]:
        return self._terminationMessagePath

    @property
    def terminationMessagePolicy(
        self,
    ) -> Optional[Literal["FallbackToLogsOnError", "File"]]:
        return self._terminationMessagePolicy

    @property
    def tty(self) -> Optional[bool]:
        return self._tty

    @property
    def volumeDevices(self) -> Optional[List[io__k8s__api__core__v1__VolumeDevice]]:
        return self._volumeDevices

    @property
    def volumeMounts(self) -> Optional[List[io__k8s__api__core__v1__VolumeMount]]:
        return self._volumeMounts

    @property
    def workingDir(self) -> Optional[str]:
        return self._workingDir

    def __init__(
        self,
        name: str,
        args: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        env: Optional[List[io__k8s__api__core__v1__EnvVar]] = None,
        envFrom: Optional[List[io__k8s__api__core__v1__EnvFromSource]] = None,
        image: Optional[str] = None,
        imagePullPolicy: Optional[Literal["Always", "IfNotPresent", "Never"]] = None,
        lifecycle: Optional[io__k8s__api__core__v1__Lifecycle] = None,
        livenessProbe: Optional[io__k8s__api__core__v1__Probe] = None,
        ports: Optional[List[io__k8s__api__core__v1__ContainerPort]] = None,
        readinessProbe: Optional[io__k8s__api__core__v1__Probe] = None,
        resources: Optional[io__k8s__api__core__v1__ResourceRequirements] = None,
        securityContext: Optional[io__k8s__api__core__v1__SecurityContext] = None,
        startupProbe: Optional[io__k8s__api__core__v1__Probe] = None,
        stdin: Optional[bool] = None,
        stdinOnce: Optional[bool] = None,
        targetContainerName: Optional[str] = None,
        terminationMessagePath: Optional[str] = None,
        terminationMessagePolicy: Optional[
            Literal["FallbackToLogsOnError", "File"]
        ] = None,
        tty: Optional[bool] = None,
        volumeDevices: Optional[List[io__k8s__api__core__v1__VolumeDevice]] = None,
        volumeMounts: Optional[List[io__k8s__api__core__v1__VolumeMount]] = None,
        workingDir: Optional[str] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if args is not None:
            self._args = args
        if command is not None:
            self._command = command
        if env is not None:
            self._env = env
        if envFrom is not None:
            self._envFrom = envFrom
        if image is not None:
            self._image = image
        if imagePullPolicy is not None:
            self._imagePullPolicy = imagePullPolicy
        if lifecycle is not None:
            self._lifecycle = lifecycle
        if livenessProbe is not None:
            self._livenessProbe = livenessProbe
        if ports is not None:
            self._ports = ports
        if readinessProbe is not None:
            self._readinessProbe = readinessProbe
        if resources is not None:
            self._resources = resources
        if securityContext is not None:
            self._securityContext = securityContext
        if startupProbe is not None:
            self._startupProbe = startupProbe
        if stdin is not None:
            self._stdin = stdin
        if stdinOnce is not None:
            self._stdinOnce = stdinOnce
        if targetContainerName is not None:
            self._targetContainerName = targetContainerName
        if terminationMessagePath is not None:
            self._terminationMessagePath = terminationMessagePath
        if terminationMessagePolicy is not None:
            self._terminationMessagePolicy = terminationMessagePolicy
        if tty is not None:
            self._tty = tty
        if volumeDevices is not None:
            self._volumeDevices = volumeDevices
        if volumeMounts is not None:
            self._volumeMounts = volumeMounts
        if workingDir is not None:
            self._workingDir = workingDir


class io__k8s__api__core__v1__ProjectedVolumeSource(K8STemplatable):
    """Represents a projected volume source"""

    props: List[str] = ["defaultMode", "sources"]
    required_props: List[str] = []

    @property
    def defaultMode(self) -> Optional[int]:
        return self._defaultMode

    @property
    def sources(self) -> Optional[List[io__k8s__api__core__v1__VolumeProjection]]:
        return self._sources

    def __init__(
        self,
        defaultMode: Optional[int] = None,
        sources: Optional[List[io__k8s__api__core__v1__VolumeProjection]] = None,
    ):
        super().__init__()
        if defaultMode is not None:
            self._defaultMode = defaultMode
        if sources is not None:
            self._sources = sources


class io__k8s__api__core__v1__Volume(K8STemplatable):
    """Volume represents a named volume in a pod that may be accessed by any container in the pod."""

    props: List[str] = [
        "awsElasticBlockStore",
        "azureDisk",
        "azureFile",
        "cephfs",
        "cinder",
        "configMap",
        "csi",
        "downwardAPI",
        "emptyDir",
        "ephemeral",
        "fc",
        "flexVolume",
        "flocker",
        "gcePersistentDisk",
        "gitRepo",
        "glusterfs",
        "hostPath",
        "iscsi",
        "name",
        "nfs",
        "persistentVolumeClaim",
        "photonPersistentDisk",
        "portworxVolume",
        "projected",
        "quobyte",
        "rbd",
        "scaleIO",
        "secret",
        "storageos",
        "vsphereVolume",
    ]
    required_props: List[str] = ["name"]

    @property
    def awsElasticBlockStore(
        self,
    ) -> Optional[io__k8s__api__core__v1__AWSElasticBlockStoreVolumeSource]:
        return self._awsElasticBlockStore

    @property
    def azureDisk(self) -> Optional[io__k8s__api__core__v1__AzureDiskVolumeSource]:
        return self._azureDisk

    @property
    def azureFile(self) -> Optional[io__k8s__api__core__v1__AzureFileVolumeSource]:
        return self._azureFile

    @property
    def cephfs(self) -> Optional[io__k8s__api__core__v1__CephFSVolumeSource]:
        return self._cephfs

    @property
    def cinder(self) -> Optional[io__k8s__api__core__v1__CinderVolumeSource]:
        return self._cinder

    @property
    def configMap(self) -> Optional[io__k8s__api__core__v1__ConfigMapVolumeSource]:
        return self._configMap

    @property
    def csi(self) -> Optional[io__k8s__api__core__v1__CSIVolumeSource]:
        return self._csi

    @property
    def downwardAPI(self) -> Optional[io__k8s__api__core__v1__DownwardAPIVolumeSource]:
        return self._downwardAPI

    @property
    def emptyDir(self) -> Optional[io__k8s__api__core__v1__EmptyDirVolumeSource]:
        return self._emptyDir

    @property
    def ephemeral(self) -> Optional[io__k8s__api__core__v1__EphemeralVolumeSource]:
        return self._ephemeral

    @property
    def fc(self) -> Optional[io__k8s__api__core__v1__FCVolumeSource]:
        return self._fc

    @property
    def flexVolume(self) -> Optional[io__k8s__api__core__v1__FlexVolumeSource]:
        return self._flexVolume

    @property
    def flocker(self) -> Optional[io__k8s__api__core__v1__FlockerVolumeSource]:
        return self._flocker

    @property
    def gcePersistentDisk(
        self,
    ) -> Optional[io__k8s__api__core__v1__GCEPersistentDiskVolumeSource]:
        return self._gcePersistentDisk

    @property
    def gitRepo(self) -> Optional[io__k8s__api__core__v1__GitRepoVolumeSource]:
        return self._gitRepo

    @property
    def glusterfs(self) -> Optional[io__k8s__api__core__v1__GlusterfsVolumeSource]:
        return self._glusterfs

    @property
    def hostPath(self) -> Optional[io__k8s__api__core__v1__HostPathVolumeSource]:
        return self._hostPath

    @property
    def iscsi(self) -> Optional[io__k8s__api__core__v1__ISCSIVolumeSource]:
        return self._iscsi

    @property
    def name(self) -> str:
        return self._name

    @property
    def nfs(self) -> Optional[io__k8s__api__core__v1__NFSVolumeSource]:
        return self._nfs

    @property
    def persistentVolumeClaim(
        self,
    ) -> Optional[io__k8s__api__core__v1__PersistentVolumeClaimVolumeSource]:
        return self._persistentVolumeClaim

    @property
    def photonPersistentDisk(
        self,
    ) -> Optional[io__k8s__api__core__v1__PhotonPersistentDiskVolumeSource]:
        return self._photonPersistentDisk

    @property
    def portworxVolume(self) -> Optional[io__k8s__api__core__v1__PortworxVolumeSource]:
        return self._portworxVolume

    @property
    def projected(self) -> Optional[io__k8s__api__core__v1__ProjectedVolumeSource]:
        return self._projected

    @property
    def quobyte(self) -> Optional[io__k8s__api__core__v1__QuobyteVolumeSource]:
        return self._quobyte

    @property
    def rbd(self) -> Optional[io__k8s__api__core__v1__RBDVolumeSource]:
        return self._rbd

    @property
    def scaleIO(self) -> Optional[io__k8s__api__core__v1__ScaleIOVolumeSource]:
        return self._scaleIO

    @property
    def secret(self) -> Optional[io__k8s__api__core__v1__SecretVolumeSource]:
        return self._secret

    @property
    def storageos(self) -> Optional[io__k8s__api__core__v1__StorageOSVolumeSource]:
        return self._storageos

    @property
    def vsphereVolume(
        self,
    ) -> Optional[io__k8s__api__core__v1__VsphereVirtualDiskVolumeSource]:
        return self._vsphereVolume

    def __init__(
        self,
        name: str,
        awsElasticBlockStore: Optional[
            io__k8s__api__core__v1__AWSElasticBlockStoreVolumeSource
        ] = None,
        azureDisk: Optional[io__k8s__api__core__v1__AzureDiskVolumeSource] = None,
        azureFile: Optional[io__k8s__api__core__v1__AzureFileVolumeSource] = None,
        cephfs: Optional[io__k8s__api__core__v1__CephFSVolumeSource] = None,
        cinder: Optional[io__k8s__api__core__v1__CinderVolumeSource] = None,
        configMap: Optional[io__k8s__api__core__v1__ConfigMapVolumeSource] = None,
        csi: Optional[io__k8s__api__core__v1__CSIVolumeSource] = None,
        downwardAPI: Optional[io__k8s__api__core__v1__DownwardAPIVolumeSource] = None,
        emptyDir: Optional[io__k8s__api__core__v1__EmptyDirVolumeSource] = None,
        ephemeral: Optional[io__k8s__api__core__v1__EphemeralVolumeSource] = None,
        fc: Optional[io__k8s__api__core__v1__FCVolumeSource] = None,
        flexVolume: Optional[io__k8s__api__core__v1__FlexVolumeSource] = None,
        flocker: Optional[io__k8s__api__core__v1__FlockerVolumeSource] = None,
        gcePersistentDisk: Optional[
            io__k8s__api__core__v1__GCEPersistentDiskVolumeSource
        ] = None,
        gitRepo: Optional[io__k8s__api__core__v1__GitRepoVolumeSource] = None,
        glusterfs: Optional[io__k8s__api__core__v1__GlusterfsVolumeSource] = None,
        hostPath: Optional[io__k8s__api__core__v1__HostPathVolumeSource] = None,
        iscsi: Optional[io__k8s__api__core__v1__ISCSIVolumeSource] = None,
        nfs: Optional[io__k8s__api__core__v1__NFSVolumeSource] = None,
        persistentVolumeClaim: Optional[
            io__k8s__api__core__v1__PersistentVolumeClaimVolumeSource
        ] = None,
        photonPersistentDisk: Optional[
            io__k8s__api__core__v1__PhotonPersistentDiskVolumeSource
        ] = None,
        portworxVolume: Optional[io__k8s__api__core__v1__PortworxVolumeSource] = None,
        projected: Optional[io__k8s__api__core__v1__ProjectedVolumeSource] = None,
        quobyte: Optional[io__k8s__api__core__v1__QuobyteVolumeSource] = None,
        rbd: Optional[io__k8s__api__core__v1__RBDVolumeSource] = None,
        scaleIO: Optional[io__k8s__api__core__v1__ScaleIOVolumeSource] = None,
        secret: Optional[io__k8s__api__core__v1__SecretVolumeSource] = None,
        storageos: Optional[io__k8s__api__core__v1__StorageOSVolumeSource] = None,
        vsphereVolume: Optional[
            io__k8s__api__core__v1__VsphereVirtualDiskVolumeSource
        ] = None,
    ):
        super().__init__()
        if name is not None:
            self._name = name
        if awsElasticBlockStore is not None:
            self._awsElasticBlockStore = awsElasticBlockStore
        if azureDisk is not None:
            self._azureDisk = azureDisk
        if azureFile is not None:
            self._azureFile = azureFile
        if cephfs is not None:
            self._cephfs = cephfs
        if cinder is not None:
            self._cinder = cinder
        if configMap is not None:
            self._configMap = configMap
        if csi is not None:
            self._csi = csi
        if downwardAPI is not None:
            self._downwardAPI = downwardAPI
        if emptyDir is not None:
            self._emptyDir = emptyDir
        if ephemeral is not None:
            self._ephemeral = ephemeral
        if fc is not None:
            self._fc = fc
        if flexVolume is not None:
            self._flexVolume = flexVolume
        if flocker is not None:
            self._flocker = flocker
        if gcePersistentDisk is not None:
            self._gcePersistentDisk = gcePersistentDisk
        if gitRepo is not None:
            self._gitRepo = gitRepo
        if glusterfs is not None:
            self._glusterfs = glusterfs
        if hostPath is not None:
            self._hostPath = hostPath
        if iscsi is not None:
            self._iscsi = iscsi
        if nfs is not None:
            self._nfs = nfs
        if persistentVolumeClaim is not None:
            self._persistentVolumeClaim = persistentVolumeClaim
        if photonPersistentDisk is not None:
            self._photonPersistentDisk = photonPersistentDisk
        if portworxVolume is not None:
            self._portworxVolume = portworxVolume
        if projected is not None:
            self._projected = projected
        if quobyte is not None:
            self._quobyte = quobyte
        if rbd is not None:
            self._rbd = rbd
        if scaleIO is not None:
            self._scaleIO = scaleIO
        if secret is not None:
            self._secret = secret
        if storageos is not None:
            self._storageos = storageos
        if vsphereVolume is not None:
            self._vsphereVolume = vsphereVolume


class io__k8s__api__flowcontrol__v1beta1__FlowSchema(K8STemplatable):
    """FlowSchema defines the schema of a group of flows. Note that a flow is made up of a set of inbound API requests with similar attributes and is identified by a pair of strings: the name of the FlowSchema and a "flow distinguisher"."""

    apiVersion: str = "flowcontrol.apiserver.k8s.io/v1beta1"
    kind: str = "FlowSchema"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__flowcontrol__v1beta1__FlowSchemaSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__flowcontrol__v1beta1__FlowSchemaStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__flowcontrol__v1beta1__FlowSchemaSpec] = None,
        status: Optional[io__k8s__api__flowcontrol__v1beta1__FlowSchemaStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__flowcontrol__v1beta1__FlowSchemaList(K8STemplatable):
    """FlowSchemaList is a list of FlowSchema objects."""

    apiVersion: str = "flowcontrol.apiserver.k8s.io/v1beta1"
    kind: str = "FlowSchemaList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__flowcontrol__v1beta1__FlowSchema]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__flowcontrol__v1beta1__FlowSchema],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__flowcontrol__v1beta2__FlowSchema(K8STemplatable):
    """FlowSchema defines the schema of a group of flows. Note that a flow is made up of a set of inbound API requests with similar attributes and is identified by a pair of strings: the name of the FlowSchema and a "flow distinguisher"."""

    apiVersion: str = "flowcontrol.apiserver.k8s.io/v1beta2"
    kind: str = "FlowSchema"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__flowcontrol__v1beta2__FlowSchemaSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__flowcontrol__v1beta2__FlowSchemaStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__flowcontrol__v1beta2__FlowSchemaSpec] = None,
        status: Optional[io__k8s__api__flowcontrol__v1beta2__FlowSchemaStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__flowcontrol__v1beta2__FlowSchemaList(K8STemplatable):
    """FlowSchemaList is a list of FlowSchema objects."""

    apiVersion: str = "flowcontrol.apiserver.k8s.io/v1beta2"
    kind: str = "FlowSchemaList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__flowcontrol__v1beta2__FlowSchema]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__flowcontrol__v1beta2__FlowSchema],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__networking__v1__Ingress(K8STemplatable):
    """Ingress is a collection of rules that allow inbound connections to reach the endpoints defined by a backend. An Ingress can be configured to give services externally-reachable urls, load balance traffic, terminate SSL, offer name based virtual hosting etc."""

    apiVersion: str = "networking.k8s.io/v1"
    kind: str = "Ingress"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__networking__v1__IngressSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__networking__v1__IngressStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__networking__v1__IngressSpec] = None,
        status: Optional[io__k8s__api__networking__v1__IngressStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__networking__v1__IngressList(K8STemplatable):
    """IngressList is a collection of Ingress."""

    apiVersion: str = "networking.k8s.io/v1"
    kind: str = "IngressList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__networking__v1__Ingress]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__networking__v1__Ingress],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__networking__v1__NetworkPolicy(K8STemplatable):
    """NetworkPolicy describes what network traffic is allowed for a set of Pods"""

    apiVersion: str = "networking.k8s.io/v1"
    kind: str = "NetworkPolicy"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__networking__v1__NetworkPolicySpec]:
        return self._spec

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__networking__v1__NetworkPolicySpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec


class io__k8s__api__networking__v1__NetworkPolicyList(K8STemplatable):
    """NetworkPolicyList is a list of NetworkPolicy objects."""

    apiVersion: str = "networking.k8s.io/v1"
    kind: str = "NetworkPolicyList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__networking__v1__NetworkPolicy]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__networking__v1__NetworkPolicy],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionSpec(
    K8STemplatable
):
    """CustomResourceDefinitionSpec describes how a user wants their resource to appear"""

    props: List[str] = [
        "conversion",
        "group",
        "names",
        "preserveUnknownFields",
        "scope",
        "versions",
    ]
    required_props: List[str] = ["group", "names", "scope", "versions"]

    @property
    def conversion(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceConversion
    ]:
        return self._conversion

    @property
    def group(self) -> str:
        return self._group

    @property
    def names(
        self,
    ) -> io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionNames:
        return self._names

    @property
    def preserveUnknownFields(self) -> Optional[bool]:
        return self._preserveUnknownFields

    @property
    def scope(self) -> str:
        return self._scope

    @property
    def versions(
        self,
    ) -> List[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionVersion
    ]:
        return self._versions

    def __init__(
        self,
        group: str,
        names: io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionNames,
        scope: str,
        versions: List[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionVersion
        ],
        conversion: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceConversion
        ] = None,
        preserveUnknownFields: Optional[bool] = None,
    ):
        super().__init__()
        if group is not None:
            self._group = group
        if names is not None:
            self._names = names
        if scope is not None:
            self._scope = scope
        if versions is not None:
            self._versions = versions
        if conversion is not None:
            self._conversion = conversion
        if preserveUnknownFields is not None:
            self._preserveUnknownFields = preserveUnknownFields


class io__k8s__api__autoscaling__v2__HorizontalPodAutoscaler(K8STemplatable):
    """HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler, which automatically manages the replica count of any resource implementing the scale subresource based on the metrics specified."""

    apiVersion: str = "autoscaling/v2"
    kind: str = "HorizontalPodAutoscaler"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerSpec]:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[
            io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerSpec
        ] = None,
        status: Optional[
            io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerStatus
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerList(K8STemplatable):
    """HorizontalPodAutoscalerList is a list of horizontal pod autoscaler objects."""

    apiVersion: str = "autoscaling/v2"
    kind: str = "HorizontalPodAutoscalerList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__autoscaling__v2__HorizontalPodAutoscaler]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__autoscaling__v2__HorizontalPodAutoscaler],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscaler(K8STemplatable):
    """HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler, which automatically manages the replica count of any resource implementing the scale subresource based on the metrics specified."""

    apiVersion: str = "autoscaling/v2beta1"
    kind: str = "HorizontalPodAutoscaler"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerSpec]:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[
            io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerSpec
        ] = None,
        status: Optional[
            io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerStatus
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerList(K8STemplatable):
    """HorizontalPodAutoscaler is a list of horizontal pod autoscaler objects."""

    apiVersion: str = "autoscaling/v2beta1"
    kind: str = "HorizontalPodAutoscalerList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(
        self,
    ) -> List[io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscaler]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscaler],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscaler(K8STemplatable):
    """HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler, which automatically manages the replica count of any resource implementing the scale subresource based on the metrics specified."""

    apiVersion: str = "autoscaling/v2beta2"
    kind: str = "HorizontalPodAutoscaler"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerSpec]:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[
            io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerSpec
        ] = None,
        status: Optional[
            io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerStatus
        ] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerList(K8STemplatable):
    """HorizontalPodAutoscalerList is a list of horizontal pod autoscaler objects."""

    apiVersion: str = "autoscaling/v2beta2"
    kind: str = "HorizontalPodAutoscalerList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(
        self,
    ) -> List[io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscaler]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscaler],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__PodSpec(K8STemplatable):
    """PodSpec is a description of a pod."""

    props: List[str] = [
        "activeDeadlineSeconds",
        "affinity",
        "automountServiceAccountToken",
        "containers",
        "dnsConfig",
        "dnsPolicy",
        "enableServiceLinks",
        "ephemeralContainers",
        "hostAliases",
        "hostIPC",
        "hostNetwork",
        "hostPID",
        "hostname",
        "imagePullSecrets",
        "initContainers",
        "nodeName",
        "nodeSelector",
        "os",
        "overhead",
        "preemptionPolicy",
        "priority",
        "priorityClassName",
        "readinessGates",
        "restartPolicy",
        "runtimeClassName",
        "schedulerName",
        "securityContext",
        "serviceAccount",
        "serviceAccountName",
        "setHostnameAsFQDN",
        "shareProcessNamespace",
        "subdomain",
        "terminationGracePeriodSeconds",
        "tolerations",
        "topologySpreadConstraints",
        "volumes",
    ]
    required_props: List[str] = ["containers"]

    @property
    def activeDeadlineSeconds(self) -> Optional[int]:
        return self._activeDeadlineSeconds

    @property
    def affinity(self) -> Optional[io__k8s__api__core__v1__Affinity]:
        return self._affinity

    @property
    def automountServiceAccountToken(self) -> Optional[bool]:
        return self._automountServiceAccountToken

    @property
    def containers(self) -> List[io__k8s__api__core__v1__Container]:
        return self._containers

    @property
    def dnsConfig(self) -> Optional[io__k8s__api__core__v1__PodDNSConfig]:
        return self._dnsConfig

    @property
    def dnsPolicy(
        self,
    ) -> Optional[
        Literal["ClusterFirst", "ClusterFirstWithHostNet", "Default", "None"]
    ]:
        return self._dnsPolicy

    @property
    def enableServiceLinks(self) -> Optional[bool]:
        return self._enableServiceLinks

    @property
    def ephemeralContainers(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__EphemeralContainer]]:
        return self._ephemeralContainers

    @property
    def hostAliases(self) -> Optional[List[io__k8s__api__core__v1__HostAlias]]:
        return self._hostAliases

    @property
    def hostIPC(self) -> Optional[bool]:
        return self._hostIPC

    @property
    def hostNetwork(self) -> Optional[bool]:
        return self._hostNetwork

    @property
    def hostPID(self) -> Optional[bool]:
        return self._hostPID

    @property
    def hostname(self) -> Optional[str]:
        return self._hostname

    @property
    def imagePullSecrets(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__LocalObjectReference]]:
        return self._imagePullSecrets

    @property
    def initContainers(self) -> Optional[List[io__k8s__api__core__v1__Container]]:
        return self._initContainers

    @property
    def nodeName(self) -> Optional[str]:
        return self._nodeName

    @property
    def nodeSelector(self) -> Optional[Dict[str, str]]:
        return self._nodeSelector

    @property
    def os(self) -> Optional[io__k8s__api__core__v1__PodOS]:
        return self._os

    @property
    def overhead(
        self,
    ) -> Optional[Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]]:
        return self._overhead

    @property
    def preemptionPolicy(self) -> Optional[str]:
        return self._preemptionPolicy

    @property
    def priority(self) -> Optional[int]:
        return self._priority

    @property
    def priorityClassName(self) -> Optional[str]:
        return self._priorityClassName

    @property
    def readinessGates(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__PodReadinessGate]]:
        return self._readinessGates

    @property
    def restartPolicy(self) -> Optional[Literal["Always", "Never", "OnFailure"]]:
        return self._restartPolicy

    @property
    def runtimeClassName(self) -> Optional[str]:
        return self._runtimeClassName

    @property
    def schedulerName(self) -> Optional[str]:
        return self._schedulerName

    @property
    def securityContext(self) -> Optional[io__k8s__api__core__v1__PodSecurityContext]:
        return self._securityContext

    @property
    def serviceAccount(self) -> Optional[str]:
        return self._serviceAccount

    @property
    def serviceAccountName(self) -> Optional[str]:
        return self._serviceAccountName

    @property
    def setHostnameAsFQDN(self) -> Optional[bool]:
        return self._setHostnameAsFQDN

    @property
    def shareProcessNamespace(self) -> Optional[bool]:
        return self._shareProcessNamespace

    @property
    def subdomain(self) -> Optional[str]:
        return self._subdomain

    @property
    def terminationGracePeriodSeconds(self) -> Optional[int]:
        return self._terminationGracePeriodSeconds

    @property
    def tolerations(self) -> Optional[List[io__k8s__api__core__v1__Toleration]]:
        return self._tolerations

    @property
    def topologySpreadConstraints(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__TopologySpreadConstraint]]:
        return self._topologySpreadConstraints

    @property
    def volumes(self) -> Optional[List[io__k8s__api__core__v1__Volume]]:
        return self._volumes

    def __init__(
        self,
        containers: List[io__k8s__api__core__v1__Container],
        activeDeadlineSeconds: Optional[int] = None,
        affinity: Optional[io__k8s__api__core__v1__Affinity] = None,
        automountServiceAccountToken: Optional[bool] = None,
        dnsConfig: Optional[io__k8s__api__core__v1__PodDNSConfig] = None,
        dnsPolicy: Optional[
            Literal["ClusterFirst", "ClusterFirstWithHostNet", "Default", "None"]
        ] = None,
        enableServiceLinks: Optional[bool] = None,
        ephemeralContainers: Optional[
            List[io__k8s__api__core__v1__EphemeralContainer]
        ] = None,
        hostAliases: Optional[List[io__k8s__api__core__v1__HostAlias]] = None,
        hostIPC: Optional[bool] = None,
        hostNetwork: Optional[bool] = None,
        hostPID: Optional[bool] = None,
        hostname: Optional[str] = None,
        imagePullSecrets: Optional[
            List[io__k8s__api__core__v1__LocalObjectReference]
        ] = None,
        initContainers: Optional[List[io__k8s__api__core__v1__Container]] = None,
        nodeName: Optional[str] = None,
        nodeSelector: Optional[Dict[str, str]] = None,
        os: Optional[io__k8s__api__core__v1__PodOS] = None,
        overhead: Optional[
            Dict[str, io__k8s__apimachinery__pkg__api__resource__Quantity]
        ] = None,
        preemptionPolicy: Optional[str] = None,
        priority: Optional[int] = None,
        priorityClassName: Optional[str] = None,
        readinessGates: Optional[List[io__k8s__api__core__v1__PodReadinessGate]] = None,
        restartPolicy: Optional[Literal["Always", "Never", "OnFailure"]] = None,
        runtimeClassName: Optional[str] = None,
        schedulerName: Optional[str] = None,
        securityContext: Optional[io__k8s__api__core__v1__PodSecurityContext] = None,
        serviceAccount: Optional[str] = None,
        serviceAccountName: Optional[str] = None,
        setHostnameAsFQDN: Optional[bool] = None,
        shareProcessNamespace: Optional[bool] = None,
        subdomain: Optional[str] = None,
        terminationGracePeriodSeconds: Optional[int] = None,
        tolerations: Optional[List[io__k8s__api__core__v1__Toleration]] = None,
        topologySpreadConstraints: Optional[
            List[io__k8s__api__core__v1__TopologySpreadConstraint]
        ] = None,
        volumes: Optional[List[io__k8s__api__core__v1__Volume]] = None,
    ):
        super().__init__()
        if containers is not None:
            self._containers = containers
        if activeDeadlineSeconds is not None:
            self._activeDeadlineSeconds = activeDeadlineSeconds
        if affinity is not None:
            self._affinity = affinity
        if automountServiceAccountToken is not None:
            self._automountServiceAccountToken = automountServiceAccountToken
        if dnsConfig is not None:
            self._dnsConfig = dnsConfig
        if dnsPolicy is not None:
            self._dnsPolicy = dnsPolicy
        if enableServiceLinks is not None:
            self._enableServiceLinks = enableServiceLinks
        if ephemeralContainers is not None:
            self._ephemeralContainers = ephemeralContainers
        if hostAliases is not None:
            self._hostAliases = hostAliases
        if hostIPC is not None:
            self._hostIPC = hostIPC
        if hostNetwork is not None:
            self._hostNetwork = hostNetwork
        if hostPID is not None:
            self._hostPID = hostPID
        if hostname is not None:
            self._hostname = hostname
        if imagePullSecrets is not None:
            self._imagePullSecrets = imagePullSecrets
        if initContainers is not None:
            self._initContainers = initContainers
        if nodeName is not None:
            self._nodeName = nodeName
        if nodeSelector is not None:
            self._nodeSelector = nodeSelector
        if os is not None:
            self._os = os
        if overhead is not None:
            self._overhead = overhead
        if preemptionPolicy is not None:
            self._preemptionPolicy = preemptionPolicy
        if priority is not None:
            self._priority = priority
        if priorityClassName is not None:
            self._priorityClassName = priorityClassName
        if readinessGates is not None:
            self._readinessGates = readinessGates
        if restartPolicy is not None:
            self._restartPolicy = restartPolicy
        if runtimeClassName is not None:
            self._runtimeClassName = runtimeClassName
        if schedulerName is not None:
            self._schedulerName = schedulerName
        if securityContext is not None:
            self._securityContext = securityContext
        if serviceAccount is not None:
            self._serviceAccount = serviceAccount
        if serviceAccountName is not None:
            self._serviceAccountName = serviceAccountName
        if setHostnameAsFQDN is not None:
            self._setHostnameAsFQDN = setHostnameAsFQDN
        if shareProcessNamespace is not None:
            self._shareProcessNamespace = shareProcessNamespace
        if subdomain is not None:
            self._subdomain = subdomain
        if terminationGracePeriodSeconds is not None:
            self._terminationGracePeriodSeconds = terminationGracePeriodSeconds
        if tolerations is not None:
            self._tolerations = tolerations
        if topologySpreadConstraints is not None:
            self._topologySpreadConstraints = topologySpreadConstraints
        if volumes is not None:
            self._volumes = volumes


class io__k8s__api__core__v1__PodTemplateSpec(K8STemplatable):
    """PodTemplateSpec describes the data a pod should have when created from a template"""

    props: List[str] = ["metadata", "spec"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__PodSpec]:
        return self._spec

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__PodSpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec


class io__k8s__api__core__v1__ReplicationControllerSpec(K8STemplatable):
    """ReplicationControllerSpec is the specification of a replication controller."""

    props: List[str] = ["minReadySeconds", "replicas", "selector", "template"]
    required_props: List[str] = []

    @property
    def minReadySeconds(self) -> Optional[int]:
        return self._minReadySeconds

    @property
    def replicas(self) -> Optional[int]:
        return self._replicas

    @property
    def selector(self) -> Optional[Dict[str, str]]:
        return self._selector

    @property
    def template(self) -> Optional[io__k8s__api__core__v1__PodTemplateSpec]:
        return self._template

    def __init__(
        self,
        minReadySeconds: Optional[int] = None,
        replicas: Optional[int] = None,
        selector: Optional[Dict[str, str]] = None,
        template: Optional[io__k8s__api__core__v1__PodTemplateSpec] = None,
    ):
        super().__init__()
        if minReadySeconds is not None:
            self._minReadySeconds = minReadySeconds
        if replicas is not None:
            self._replicas = replicas
        if selector is not None:
            self._selector = selector
        if template is not None:
            self._template = template


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinition(
    K8STemplatable
):
    """CustomResourceDefinition represents a resource that should be exposed on the API server.  Its name MUST be in the format <.spec.name>.<.spec.group>."""

    apiVersion: str = "apiextensions.k8s.io/v1"
    kind: str = "CustomResourceDefinition"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = ["spec"]

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(
        self,
    ) -> io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionSpec:
        return self._spec

    @property
    def status(
        self,
    ) -> Optional[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionStatus
    ]:
        return self._status

    def __init__(
        self,
        spec: io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionSpec,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        status: Optional[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionStatus
        ] = None,
    ):
        super().__init__()
        if spec is not None:
            self._spec = spec
        if metadata is not None:
            self._metadata = metadata
        if status is not None:
            self._status = status


class io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionList(
    K8STemplatable
):
    """CustomResourceDefinitionList is a list of CustomResourceDefinition objects."""

    apiVersion: str = "apiextensions.k8s.io/v1"
    kind: str = "CustomResourceDefinitionList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(
        self,
    ) -> List[
        io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinition
    ]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[
            io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinition
        ],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apps__v1__DaemonSetSpec(K8STemplatable):
    """DaemonSetSpec is the specification of a daemon set."""

    props: List[str] = [
        "minReadySeconds",
        "revisionHistoryLimit",
        "selector",
        "template",
        "updateStrategy",
    ]
    required_props: List[str] = ["selector", "template"]

    @property
    def minReadySeconds(self) -> Optional[int]:
        return self._minReadySeconds

    @property
    def revisionHistoryLimit(self) -> Optional[int]:
        return self._revisionHistoryLimit

    @property
    def selector(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector:
        return self._selector

    @property
    def template(self) -> io__k8s__api__core__v1__PodTemplateSpec:
        return self._template

    @property
    def updateStrategy(
        self,
    ) -> Optional[io__k8s__api__apps__v1__DaemonSetUpdateStrategy]:
        return self._updateStrategy

    def __init__(
        self,
        selector: io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector,
        template: io__k8s__api__core__v1__PodTemplateSpec,
        minReadySeconds: Optional[int] = None,
        revisionHistoryLimit: Optional[int] = None,
        updateStrategy: Optional[
            io__k8s__api__apps__v1__DaemonSetUpdateStrategy
        ] = None,
    ):
        super().__init__()
        if selector is not None:
            self._selector = selector
        if template is not None:
            self._template = template
        if minReadySeconds is not None:
            self._minReadySeconds = minReadySeconds
        if revisionHistoryLimit is not None:
            self._revisionHistoryLimit = revisionHistoryLimit
        if updateStrategy is not None:
            self._updateStrategy = updateStrategy


class io__k8s__api__apps__v1__DeploymentSpec(K8STemplatable):
    """DeploymentSpec is the specification of the desired behavior of the Deployment."""

    props: List[str] = [
        "minReadySeconds",
        "paused",
        "progressDeadlineSeconds",
        "replicas",
        "revisionHistoryLimit",
        "selector",
        "strategy",
        "template",
    ]
    required_props: List[str] = ["selector", "template"]

    @property
    def minReadySeconds(self) -> Optional[int]:
        return self._minReadySeconds

    @property
    def paused(self) -> Optional[bool]:
        return self._paused

    @property
    def progressDeadlineSeconds(self) -> Optional[int]:
        return self._progressDeadlineSeconds

    @property
    def replicas(self) -> Optional[int]:
        return self._replicas

    @property
    def revisionHistoryLimit(self) -> Optional[int]:
        return self._revisionHistoryLimit

    @property
    def selector(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector:
        return self._selector

    @property
    def strategy(self) -> Optional[io__k8s__api__apps__v1__DeploymentStrategy]:
        return self._strategy

    @property
    def template(self) -> io__k8s__api__core__v1__PodTemplateSpec:
        return self._template

    def __init__(
        self,
        selector: io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector,
        template: io__k8s__api__core__v1__PodTemplateSpec,
        minReadySeconds: Optional[int] = None,
        paused: Optional[bool] = None,
        progressDeadlineSeconds: Optional[int] = None,
        replicas: Optional[int] = None,
        revisionHistoryLimit: Optional[int] = None,
        strategy: Optional[io__k8s__api__apps__v1__DeploymentStrategy] = None,
    ):
        super().__init__()
        if selector is not None:
            self._selector = selector
        if template is not None:
            self._template = template
        if minReadySeconds is not None:
            self._minReadySeconds = minReadySeconds
        if paused is not None:
            self._paused = paused
        if progressDeadlineSeconds is not None:
            self._progressDeadlineSeconds = progressDeadlineSeconds
        if replicas is not None:
            self._replicas = replicas
        if revisionHistoryLimit is not None:
            self._revisionHistoryLimit = revisionHistoryLimit
        if strategy is not None:
            self._strategy = strategy


class io__k8s__api__apps__v1__ReplicaSetSpec(K8STemplatable):
    """ReplicaSetSpec is the specification of a ReplicaSet."""

    props: List[str] = ["minReadySeconds", "replicas", "selector", "template"]
    required_props: List[str] = ["selector"]

    @property
    def minReadySeconds(self) -> Optional[int]:
        return self._minReadySeconds

    @property
    def replicas(self) -> Optional[int]:
        return self._replicas

    @property
    def selector(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector:
        return self._selector

    @property
    def template(self) -> Optional[io__k8s__api__core__v1__PodTemplateSpec]:
        return self._template

    def __init__(
        self,
        selector: io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector,
        minReadySeconds: Optional[int] = None,
        replicas: Optional[int] = None,
        template: Optional[io__k8s__api__core__v1__PodTemplateSpec] = None,
    ):
        super().__init__()
        if selector is not None:
            self._selector = selector
        if minReadySeconds is not None:
            self._minReadySeconds = minReadySeconds
        if replicas is not None:
            self._replicas = replicas
        if template is not None:
            self._template = template


class io__k8s__api__apps__v1__StatefulSetSpec(K8STemplatable):
    """A StatefulSetSpec is the specification of a StatefulSet."""

    props: List[str] = [
        "minReadySeconds",
        "persistentVolumeClaimRetentionPolicy",
        "podManagementPolicy",
        "replicas",
        "revisionHistoryLimit",
        "selector",
        "serviceName",
        "template",
        "updateStrategy",
        "volumeClaimTemplates",
    ]
    required_props: List[str] = ["selector", "template", "serviceName"]

    @property
    def minReadySeconds(self) -> Optional[int]:
        return self._minReadySeconds

    @property
    def persistentVolumeClaimRetentionPolicy(
        self,
    ) -> Optional[
        io__k8s__api__apps__v1__StatefulSetPersistentVolumeClaimRetentionPolicy
    ]:
        return self._persistentVolumeClaimRetentionPolicy

    @property
    def podManagementPolicy(self) -> Optional[Literal["OrderedReady", "Parallel"]]:
        return self._podManagementPolicy

    @property
    def replicas(self) -> Optional[int]:
        return self._replicas

    @property
    def revisionHistoryLimit(self) -> Optional[int]:
        return self._revisionHistoryLimit

    @property
    def selector(self) -> io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector:
        return self._selector

    @property
    def serviceName(self) -> str:
        return self._serviceName

    @property
    def template(self) -> io__k8s__api__core__v1__PodTemplateSpec:
        return self._template

    @property
    def updateStrategy(
        self,
    ) -> Optional[io__k8s__api__apps__v1__StatefulSetUpdateStrategy]:
        return self._updateStrategy

    @property
    def volumeClaimTemplates(
        self,
    ) -> Optional[List[io__k8s__api__core__v1__PersistentVolumeClaim]]:
        return self._volumeClaimTemplates

    def __init__(
        self,
        selector: io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector,
        serviceName: str,
        template: io__k8s__api__core__v1__PodTemplateSpec,
        minReadySeconds: Optional[int] = None,
        persistentVolumeClaimRetentionPolicy: Optional[
            io__k8s__api__apps__v1__StatefulSetPersistentVolumeClaimRetentionPolicy
        ] = None,
        podManagementPolicy: Optional[Literal["OrderedReady", "Parallel"]] = None,
        replicas: Optional[int] = None,
        revisionHistoryLimit: Optional[int] = None,
        updateStrategy: Optional[
            io__k8s__api__apps__v1__StatefulSetUpdateStrategy
        ] = None,
        volumeClaimTemplates: Optional[
            List[io__k8s__api__core__v1__PersistentVolumeClaim]
        ] = None,
    ):
        super().__init__()
        if selector is not None:
            self._selector = selector
        if serviceName is not None:
            self._serviceName = serviceName
        if template is not None:
            self._template = template
        if minReadySeconds is not None:
            self._minReadySeconds = minReadySeconds
        if persistentVolumeClaimRetentionPolicy is not None:
            self._persistentVolumeClaimRetentionPolicy = (
                persistentVolumeClaimRetentionPolicy
            )
        if podManagementPolicy is not None:
            self._podManagementPolicy = podManagementPolicy
        if replicas is not None:
            self._replicas = replicas
        if revisionHistoryLimit is not None:
            self._revisionHistoryLimit = revisionHistoryLimit
        if updateStrategy is not None:
            self._updateStrategy = updateStrategy
        if volumeClaimTemplates is not None:
            self._volumeClaimTemplates = volumeClaimTemplates


class io__k8s__api__batch__v1__JobSpec(K8STemplatable):
    """JobSpec describes how the job execution will look like."""

    props: List[str] = [
        "activeDeadlineSeconds",
        "backoffLimit",
        "completionMode",
        "completions",
        "manualSelector",
        "parallelism",
        "selector",
        "suspend",
        "template",
        "ttlSecondsAfterFinished",
    ]
    required_props: List[str] = ["template"]

    @property
    def activeDeadlineSeconds(self) -> Optional[int]:
        return self._activeDeadlineSeconds

    @property
    def backoffLimit(self) -> Optional[int]:
        return self._backoffLimit

    @property
    def completionMode(self) -> Optional[str]:
        return self._completionMode

    @property
    def completions(self) -> Optional[int]:
        return self._completions

    @property
    def manualSelector(self) -> Optional[bool]:
        return self._manualSelector

    @property
    def parallelism(self) -> Optional[int]:
        return self._parallelism

    @property
    def selector(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector]:
        return self._selector

    @property
    def suspend(self) -> Optional[bool]:
        return self._suspend

    @property
    def template(self) -> io__k8s__api__core__v1__PodTemplateSpec:
        return self._template

    @property
    def ttlSecondsAfterFinished(self) -> Optional[int]:
        return self._ttlSecondsAfterFinished

    def __init__(
        self,
        template: io__k8s__api__core__v1__PodTemplateSpec,
        activeDeadlineSeconds: Optional[int] = None,
        backoffLimit: Optional[int] = None,
        completionMode: Optional[str] = None,
        completions: Optional[int] = None,
        manualSelector: Optional[bool] = None,
        parallelism: Optional[int] = None,
        selector: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
        ] = None,
        suspend: Optional[bool] = None,
        ttlSecondsAfterFinished: Optional[int] = None,
    ):
        super().__init__()
        if template is not None:
            self._template = template
        if activeDeadlineSeconds is not None:
            self._activeDeadlineSeconds = activeDeadlineSeconds
        if backoffLimit is not None:
            self._backoffLimit = backoffLimit
        if completionMode is not None:
            self._completionMode = completionMode
        if completions is not None:
            self._completions = completions
        if manualSelector is not None:
            self._manualSelector = manualSelector
        if parallelism is not None:
            self._parallelism = parallelism
        if selector is not None:
            self._selector = selector
        if suspend is not None:
            self._suspend = suspend
        if ttlSecondsAfterFinished is not None:
            self._ttlSecondsAfterFinished = ttlSecondsAfterFinished


class io__k8s__api__batch__v1__JobTemplateSpec(K8STemplatable):
    """JobTemplateSpec describes the data a Job should have when created from a template"""

    props: List[str] = ["metadata", "spec"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__batch__v1__JobSpec]:
        return self._spec

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__batch__v1__JobSpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec


class io__k8s__api__batch__v1beta1__JobTemplateSpec(K8STemplatable):
    """JobTemplateSpec describes the data a Job should have when created from a template"""

    props: List[str] = ["metadata", "spec"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__batch__v1__JobSpec]:
        return self._spec

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__batch__v1__JobSpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec


class io__k8s__api__core__v1__Pod(K8STemplatable):
    """Pod is a collection of containers that can run on a host. This resource is created by clients and scheduled onto hosts."""

    apiVersion: str = "v1"
    kind: str = "Pod"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__PodSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__core__v1__PodStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__PodSpec] = None,
        status: Optional[io__k8s__api__core__v1__PodStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__core__v1__PodList(K8STemplatable):
    """PodList is a list of Pods."""

    apiVersion: str = "v1"
    kind: str = "PodList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__Pod]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__Pod],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__PodTemplate(K8STemplatable):
    """PodTemplate describes a template for creating copies of a predefined pod."""

    apiVersion: str = "v1"
    kind: str = "PodTemplate"

    props: List[str] = ["apiVersion", "kind", "metadata", "template"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def template(self) -> Optional[io__k8s__api__core__v1__PodTemplateSpec]:
        return self._template

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        template: Optional[io__k8s__api__core__v1__PodTemplateSpec] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if template is not None:
            self._template = template


class io__k8s__api__core__v1__PodTemplateList(K8STemplatable):
    """PodTemplateList is a list of PodTemplates."""

    apiVersion: str = "v1"
    kind: str = "PodTemplateList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__PodTemplate]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__PodTemplate],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__core__v1__ReplicationController(K8STemplatable):
    """ReplicationController represents the configuration of a replication controller."""

    apiVersion: str = "v1"
    kind: str = "ReplicationController"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__core__v1__ReplicationControllerSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__core__v1__ReplicationControllerStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__core__v1__ReplicationControllerSpec] = None,
        status: Optional[io__k8s__api__core__v1__ReplicationControllerStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__core__v1__ReplicationControllerList(K8STemplatable):
    """ReplicationControllerList is a collection of replication controllers."""

    apiVersion: str = "v1"
    kind: str = "ReplicationControllerList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__core__v1__ReplicationController]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__core__v1__ReplicationController],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apps__v1__DaemonSet(K8STemplatable):
    """DaemonSet represents the configuration of a daemon set."""

    apiVersion: str = "apps/v1"
    kind: str = "DaemonSet"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__apps__v1__DaemonSetSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__apps__v1__DaemonSetStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__apps__v1__DaemonSetSpec] = None,
        status: Optional[io__k8s__api__apps__v1__DaemonSetStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__apps__v1__DaemonSetList(K8STemplatable):
    """DaemonSetList is a collection of daemon sets."""

    apiVersion: str = "apps/v1"
    kind: str = "DaemonSetList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__apps__v1__DaemonSet]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__apps__v1__DaemonSet],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apps__v1__Deployment(K8STemplatable):
    """Deployment enables declarative updates for Pods and ReplicaSets."""

    apiVersion: str = "apps/v1"
    kind: str = "Deployment"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__apps__v1__DeploymentSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__apps__v1__DeploymentStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__apps__v1__DeploymentSpec] = None,
        status: Optional[io__k8s__api__apps__v1__DeploymentStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__apps__v1__DeploymentList(K8STemplatable):
    """DeploymentList is a list of Deployments."""

    apiVersion: str = "apps/v1"
    kind: str = "DeploymentList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__apps__v1__Deployment]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__apps__v1__Deployment],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apps__v1__ReplicaSet(K8STemplatable):
    """ReplicaSet ensures that a specified number of pod replicas are running at any given time."""

    apiVersion: str = "apps/v1"
    kind: str = "ReplicaSet"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__apps__v1__ReplicaSetSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__apps__v1__ReplicaSetStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__apps__v1__ReplicaSetSpec] = None,
        status: Optional[io__k8s__api__apps__v1__ReplicaSetStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__apps__v1__ReplicaSetList(K8STemplatable):
    """ReplicaSetList is a collection of ReplicaSets."""

    apiVersion: str = "apps/v1"
    kind: str = "ReplicaSetList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__apps__v1__ReplicaSet]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__apps__v1__ReplicaSet],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__apps__v1__StatefulSet(K8STemplatable):
    """StatefulSet represents a set of pods with consistent identities. Identities are defined as:
     - Network: A single stable DNS and hostname.
     - Storage: As many VolumeClaims as requested.
    The StatefulSet guarantees that a given network identity will always map to the same storage identity."""

    apiVersion: str = "apps/v1"
    kind: str = "StatefulSet"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__apps__v1__StatefulSetSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__apps__v1__StatefulSetStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__apps__v1__StatefulSetSpec] = None,
        status: Optional[io__k8s__api__apps__v1__StatefulSetStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__apps__v1__StatefulSetList(K8STemplatable):
    """StatefulSetList is a collection of StatefulSets."""

    apiVersion: str = "apps/v1"
    kind: str = "StatefulSetList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__apps__v1__StatefulSet]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__apps__v1__StatefulSet],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__batch__v1__CronJobSpec(K8STemplatable):
    """CronJobSpec describes how the job execution will look like and when it will actually run."""

    props: List[str] = [
        "concurrencyPolicy",
        "failedJobsHistoryLimit",
        "jobTemplate",
        "schedule",
        "startingDeadlineSeconds",
        "successfulJobsHistoryLimit",
        "suspend",
    ]
    required_props: List[str] = ["schedule", "jobTemplate"]

    @property
    def concurrencyPolicy(self) -> Optional[Literal["Allow", "Forbid", "Replace"]]:
        return self._concurrencyPolicy

    @property
    def failedJobsHistoryLimit(self) -> Optional[int]:
        return self._failedJobsHistoryLimit

    @property
    def jobTemplate(self) -> io__k8s__api__batch__v1__JobTemplateSpec:
        return self._jobTemplate

    @property
    def schedule(self) -> str:
        return self._schedule

    @property
    def startingDeadlineSeconds(self) -> Optional[int]:
        return self._startingDeadlineSeconds

    @property
    def successfulJobsHistoryLimit(self) -> Optional[int]:
        return self._successfulJobsHistoryLimit

    @property
    def suspend(self) -> Optional[bool]:
        return self._suspend

    def __init__(
        self,
        jobTemplate: io__k8s__api__batch__v1__JobTemplateSpec,
        schedule: str,
        concurrencyPolicy: Optional[Literal["Allow", "Forbid", "Replace"]] = None,
        failedJobsHistoryLimit: Optional[int] = None,
        startingDeadlineSeconds: Optional[int] = None,
        successfulJobsHistoryLimit: Optional[int] = None,
        suspend: Optional[bool] = None,
    ):
        super().__init__()
        if jobTemplate is not None:
            self._jobTemplate = jobTemplate
        if schedule is not None:
            self._schedule = schedule
        if concurrencyPolicy is not None:
            self._concurrencyPolicy = concurrencyPolicy
        if failedJobsHistoryLimit is not None:
            self._failedJobsHistoryLimit = failedJobsHistoryLimit
        if startingDeadlineSeconds is not None:
            self._startingDeadlineSeconds = startingDeadlineSeconds
        if successfulJobsHistoryLimit is not None:
            self._successfulJobsHistoryLimit = successfulJobsHistoryLimit
        if suspend is not None:
            self._suspend = suspend


class io__k8s__api__batch__v1__Job(K8STemplatable):
    """Job represents the configuration of a single job."""

    apiVersion: str = "batch/v1"
    kind: str = "Job"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__batch__v1__JobSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__batch__v1__JobStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__batch__v1__JobSpec] = None,
        status: Optional[io__k8s__api__batch__v1__JobStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__batch__v1__JobList(K8STemplatable):
    """JobList is a collection of jobs."""

    apiVersion: str = "batch/v1"
    kind: str = "JobList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__batch__v1__Job]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__batch__v1__Job],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__batch__v1beta1__CronJobSpec(K8STemplatable):
    """CronJobSpec describes how the job execution will look like and when it will actually run."""

    props: List[str] = [
        "concurrencyPolicy",
        "failedJobsHistoryLimit",
        "jobTemplate",
        "schedule",
        "startingDeadlineSeconds",
        "successfulJobsHistoryLimit",
        "suspend",
    ]
    required_props: List[str] = ["schedule", "jobTemplate"]

    @property
    def concurrencyPolicy(self) -> Optional[str]:
        return self._concurrencyPolicy

    @property
    def failedJobsHistoryLimit(self) -> Optional[int]:
        return self._failedJobsHistoryLimit

    @property
    def jobTemplate(self) -> io__k8s__api__batch__v1beta1__JobTemplateSpec:
        return self._jobTemplate

    @property
    def schedule(self) -> str:
        return self._schedule

    @property
    def startingDeadlineSeconds(self) -> Optional[int]:
        return self._startingDeadlineSeconds

    @property
    def successfulJobsHistoryLimit(self) -> Optional[int]:
        return self._successfulJobsHistoryLimit

    @property
    def suspend(self) -> Optional[bool]:
        return self._suspend

    def __init__(
        self,
        jobTemplate: io__k8s__api__batch__v1beta1__JobTemplateSpec,
        schedule: str,
        concurrencyPolicy: Optional[str] = None,
        failedJobsHistoryLimit: Optional[int] = None,
        startingDeadlineSeconds: Optional[int] = None,
        successfulJobsHistoryLimit: Optional[int] = None,
        suspend: Optional[bool] = None,
    ):
        super().__init__()
        if jobTemplate is not None:
            self._jobTemplate = jobTemplate
        if schedule is not None:
            self._schedule = schedule
        if concurrencyPolicy is not None:
            self._concurrencyPolicy = concurrencyPolicy
        if failedJobsHistoryLimit is not None:
            self._failedJobsHistoryLimit = failedJobsHistoryLimit
        if startingDeadlineSeconds is not None:
            self._startingDeadlineSeconds = startingDeadlineSeconds
        if successfulJobsHistoryLimit is not None:
            self._successfulJobsHistoryLimit = successfulJobsHistoryLimit
        if suspend is not None:
            self._suspend = suspend


class io__k8s__api__batch__v1__CronJob(K8STemplatable):
    """CronJob represents the configuration of a single cron job."""

    apiVersion: str = "batch/v1"
    kind: str = "CronJob"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__batch__v1__CronJobSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__batch__v1__CronJobStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__batch__v1__CronJobSpec] = None,
        status: Optional[io__k8s__api__batch__v1__CronJobStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__batch__v1__CronJobList(K8STemplatable):
    """CronJobList is a collection of cron jobs."""

    apiVersion: str = "batch/v1"
    kind: str = "CronJobList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__batch__v1__CronJob]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__batch__v1__CronJob],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


class io__k8s__api__batch__v1beta1__CronJob(K8STemplatable):
    """CronJob represents the configuration of a single cron job."""

    apiVersion: str = "batch/v1beta1"
    kind: str = "CronJob"

    props: List[str] = ["apiVersion", "kind", "metadata", "spec", "status"]
    required_props: List[str] = []

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta]:
        return self._metadata

    @property
    def spec(self) -> Optional[io__k8s__api__batch__v1beta1__CronJobSpec]:
        return self._spec

    @property
    def status(self) -> Optional[io__k8s__api__batch__v1beta1__CronJobStatus]:
        return self._status

    def __init__(
        self,
        metadata: Optional[
            io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
        ] = None,
        spec: Optional[io__k8s__api__batch__v1beta1__CronJobSpec] = None,
        status: Optional[io__k8s__api__batch__v1beta1__CronJobStatus] = None,
    ):
        super().__init__()
        if metadata is not None:
            self._metadata = metadata
        if spec is not None:
            self._spec = spec
        if status is not None:
            self._status = status


class io__k8s__api__batch__v1beta1__CronJobList(K8STemplatable):
    """CronJobList is a collection of cron jobs."""

    apiVersion: str = "batch/v1beta1"
    kind: str = "CronJobList"

    props: List[str] = ["apiVersion", "items", "kind", "metadata"]
    required_props: List[str] = ["items"]

    @property
    def items(self) -> List[io__k8s__api__batch__v1beta1__CronJob]:
        return self._items

    @property
    def metadata(
        self,
    ) -> Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta]:
        return self._metadata

    def __init__(
        self,
        items: List[io__k8s__api__batch__v1beta1__CronJob],
        metadata: Optional[io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta] = None,
    ):
        super().__init__()
        if items is not None:
            self._items = items
        if metadata is not None:
            self._metadata = metadata


MutatingWebhook = io__k8s__api__admissionregistration__v1__MutatingWebhook
MutatingWebhookConfiguration = (
    io__k8s__api__admissionregistration__v1__MutatingWebhookConfiguration
)
MutatingWebhookConfigurationList = (
    io__k8s__api__admissionregistration__v1__MutatingWebhookConfigurationList
)
RuleWithOperations = io__k8s__api__admissionregistration__v1__RuleWithOperations
ServiceReference = (
    io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__ServiceReference
)
ValidatingWebhook = io__k8s__api__admissionregistration__v1__ValidatingWebhook
ValidatingWebhookConfiguration = (
    io__k8s__api__admissionregistration__v1__ValidatingWebhookConfiguration
)
ValidatingWebhookConfigurationList = (
    io__k8s__api__admissionregistration__v1__ValidatingWebhookConfigurationList
)
WebhookClientConfig = (
    io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__WebhookClientConfig
)
ServerStorageVersion = io__k8s__api__apiserverinternal__v1alpha1__ServerStorageVersion
StorageVersion = io__k8s__api__apiserverinternal__v1alpha1__StorageVersion
StorageVersionCondition = (
    io__k8s__api__apiserverinternal__v1alpha1__StorageVersionCondition
)
StorageVersionList = io__k8s__api__apiserverinternal__v1alpha1__StorageVersionList
StorageVersionSpec = io__k8s__api__apiserverinternal__v1alpha1__StorageVersionSpec
StorageVersionStatus = io__k8s__api__apiserverinternal__v1alpha1__StorageVersionStatus
ControllerRevision = io__k8s__api__apps__v1__ControllerRevision
ControllerRevisionList = io__k8s__api__apps__v1__ControllerRevisionList
DaemonSet = io__k8s__api__apps__v1__DaemonSet
DaemonSetCondition = io__k8s__api__apps__v1__DaemonSetCondition
DaemonSetList = io__k8s__api__apps__v1__DaemonSetList
DaemonSetSpec = io__k8s__api__apps__v1__DaemonSetSpec
DaemonSetStatus = io__k8s__api__apps__v1__DaemonSetStatus
DaemonSetUpdateStrategy = io__k8s__api__apps__v1__DaemonSetUpdateStrategy
Deployment = io__k8s__api__apps__v1__Deployment
DeploymentCondition = io__k8s__api__apps__v1__DeploymentCondition
DeploymentList = io__k8s__api__apps__v1__DeploymentList
DeploymentSpec = io__k8s__api__apps__v1__DeploymentSpec
DeploymentStatus = io__k8s__api__apps__v1__DeploymentStatus
DeploymentStrategy = io__k8s__api__apps__v1__DeploymentStrategy
ReplicaSet = io__k8s__api__apps__v1__ReplicaSet
ReplicaSetCondition = io__k8s__api__apps__v1__ReplicaSetCondition
ReplicaSetList = io__k8s__api__apps__v1__ReplicaSetList
ReplicaSetSpec = io__k8s__api__apps__v1__ReplicaSetSpec
ReplicaSetStatus = io__k8s__api__apps__v1__ReplicaSetStatus
RollingUpdateDaemonSet = io__k8s__api__apps__v1__RollingUpdateDaemonSet
RollingUpdateDeployment = io__k8s__api__apps__v1__RollingUpdateDeployment
RollingUpdateStatefulSetStrategy = (
    io__k8s__api__apps__v1__RollingUpdateStatefulSetStrategy
)
StatefulSet = io__k8s__api__apps__v1__StatefulSet
StatefulSetCondition = io__k8s__api__apps__v1__StatefulSetCondition
StatefulSetList = io__k8s__api__apps__v1__StatefulSetList
StatefulSetPersistentVolumeClaimRetentionPolicy = (
    io__k8s__api__apps__v1__StatefulSetPersistentVolumeClaimRetentionPolicy
)
StatefulSetSpec = io__k8s__api__apps__v1__StatefulSetSpec
StatefulSetStatus = io__k8s__api__apps__v1__StatefulSetStatus
StatefulSetUpdateStrategy = io__k8s__api__apps__v1__StatefulSetUpdateStrategy
BoundObjectReference = io__k8s__api__authentication__v1__BoundObjectReference
TokenRequest = io__k8s__api__storage__v1__TokenRequest
TokenRequestSpec = io__k8s__api__authentication__v1__TokenRequestSpec
TokenRequestStatus = io__k8s__api__authentication__v1__TokenRequestStatus
TokenReview = io__k8s__api__authentication__v1__TokenReview
TokenReviewSpec = io__k8s__api__authentication__v1__TokenReviewSpec
TokenReviewStatus = io__k8s__api__authentication__v1__TokenReviewStatus
UserInfo = io__k8s__api__authentication__v1__UserInfo
LocalSubjectAccessReview = io__k8s__api__authorization__v1__LocalSubjectAccessReview
NonResourceAttributes = io__k8s__api__authorization__v1__NonResourceAttributes
NonResourceRule = io__k8s__api__authorization__v1__NonResourceRule
ResourceAttributes = io__k8s__api__authorization__v1__ResourceAttributes
ResourceRule = io__k8s__api__authorization__v1__ResourceRule
SelfSubjectAccessReview = io__k8s__api__authorization__v1__SelfSubjectAccessReview
SelfSubjectAccessReviewSpec = (
    io__k8s__api__authorization__v1__SelfSubjectAccessReviewSpec
)
SelfSubjectRulesReview = io__k8s__api__authorization__v1__SelfSubjectRulesReview
SelfSubjectRulesReviewSpec = io__k8s__api__authorization__v1__SelfSubjectRulesReviewSpec
SubjectAccessReview = io__k8s__api__authorization__v1__SubjectAccessReview
SubjectAccessReviewSpec = io__k8s__api__authorization__v1__SubjectAccessReviewSpec
SubjectAccessReviewStatus = io__k8s__api__authorization__v1__SubjectAccessReviewStatus
SubjectRulesReviewStatus = io__k8s__api__authorization__v1__SubjectRulesReviewStatus
CrossVersionObjectReference = (
    io__k8s__api__autoscaling__v2beta2__CrossVersionObjectReference
)
HorizontalPodAutoscaler = io__k8s__api__autoscaling__v1__HorizontalPodAutoscaler
HorizontalPodAutoscalerList = io__k8s__api__autoscaling__v1__HorizontalPodAutoscalerList
HorizontalPodAutoscalerSpec = (
    io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerSpec
)
HorizontalPodAutoscalerStatus = (
    io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerStatus
)
Scale = io__k8s__api__autoscaling__v1__Scale
ScaleSpec = io__k8s__api__autoscaling__v1__ScaleSpec
ScaleStatus = io__k8s__api__autoscaling__v1__ScaleStatus
ContainerResourceMetricSource = (
    io__k8s__api__autoscaling__v2beta2__ContainerResourceMetricSource
)
ContainerResourceMetricStatus = (
    io__k8s__api__autoscaling__v2beta2__ContainerResourceMetricStatus
)
ExternalMetricSource = io__k8s__api__autoscaling__v2beta2__ExternalMetricSource
ExternalMetricStatus = io__k8s__api__autoscaling__v2beta2__ExternalMetricStatus
HPAScalingPolicy = io__k8s__api__autoscaling__v2beta2__HPAScalingPolicy
HPAScalingRules = io__k8s__api__autoscaling__v2beta2__HPAScalingRules
autoscaling_v2_HorizontalPodAutoscaler = (
    io__k8s__api__autoscaling__v2__HorizontalPodAutoscaler
)
HorizontalPodAutoscalerBehavior = (
    io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerBehavior
)
HorizontalPodAutoscalerCondition = (
    io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerCondition
)
autoscaling_v2_HorizontalPodAutoscalerList = (
    io__k8s__api__autoscaling__v2__HorizontalPodAutoscalerList
)
MetricIdentifier = io__k8s__api__autoscaling__v2beta2__MetricIdentifier
MetricSpec = io__k8s__api__autoscaling__v2beta2__MetricSpec
MetricStatus = io__k8s__api__autoscaling__v2beta2__MetricStatus
MetricTarget = io__k8s__api__autoscaling__v2beta2__MetricTarget
MetricValueStatus = io__k8s__api__autoscaling__v2beta2__MetricValueStatus
ObjectMetricSource = io__k8s__api__autoscaling__v2beta2__ObjectMetricSource
ObjectMetricStatus = io__k8s__api__autoscaling__v2beta2__ObjectMetricStatus
PodsMetricSource = io__k8s__api__autoscaling__v2beta2__PodsMetricSource
PodsMetricStatus = io__k8s__api__autoscaling__v2beta2__PodsMetricStatus
ResourceMetricSource = io__k8s__api__autoscaling__v2beta2__ResourceMetricSource
ResourceMetricStatus = io__k8s__api__autoscaling__v2beta2__ResourceMetricStatus
autoscaling_v2beta1_HorizontalPodAutoscaler = (
    io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscaler
)
autoscaling_v2beta1_HorizontalPodAutoscalerList = (
    io__k8s__api__autoscaling__v2beta1__HorizontalPodAutoscalerList
)
autoscaling_v2beta2_HorizontalPodAutoscaler = (
    io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscaler
)
autoscaling_v2beta2_HorizontalPodAutoscalerList = (
    io__k8s__api__autoscaling__v2beta2__HorizontalPodAutoscalerList
)
CronJob = io__k8s__api__batch__v1__CronJob
CronJobList = io__k8s__api__batch__v1__CronJobList
CronJobSpec = io__k8s__api__batch__v1beta1__CronJobSpec
CronJobStatus = io__k8s__api__batch__v1beta1__CronJobStatus
Job = io__k8s__api__batch__v1__Job
JobCondition = io__k8s__api__batch__v1__JobCondition
JobList = io__k8s__api__batch__v1__JobList
JobSpec = io__k8s__api__batch__v1__JobSpec
JobStatus = io__k8s__api__batch__v1__JobStatus
JobTemplateSpec = io__k8s__api__batch__v1beta1__JobTemplateSpec
UncountedTerminatedPods = io__k8s__api__batch__v1__UncountedTerminatedPods
batch_v1beta1_CronJob = io__k8s__api__batch__v1beta1__CronJob
batch_v1beta1_CronJobList = io__k8s__api__batch__v1beta1__CronJobList
CertificateSigningRequest = io__k8s__api__certificates__v1__CertificateSigningRequest
CertificateSigningRequestCondition = (
    io__k8s__api__certificates__v1__CertificateSigningRequestCondition
)
CertificateSigningRequestList = (
    io__k8s__api__certificates__v1__CertificateSigningRequestList
)
CertificateSigningRequestSpec = (
    io__k8s__api__certificates__v1__CertificateSigningRequestSpec
)
CertificateSigningRequestStatus = (
    io__k8s__api__certificates__v1__CertificateSigningRequestStatus
)
Lease = io__k8s__api__coordination__v1__Lease
LeaseList = io__k8s__api__coordination__v1__LeaseList
LeaseSpec = io__k8s__api__coordination__v1__LeaseSpec
AWSElasticBlockStoreVolumeSource = (
    io__k8s__api__core__v1__AWSElasticBlockStoreVolumeSource
)
Affinity = io__k8s__api__core__v1__Affinity
AttachedVolume = io__k8s__api__core__v1__AttachedVolume
AzureDiskVolumeSource = io__k8s__api__core__v1__AzureDiskVolumeSource
AzureFilePersistentVolumeSource = (
    io__k8s__api__core__v1__AzureFilePersistentVolumeSource
)
AzureFileVolumeSource = io__k8s__api__core__v1__AzureFileVolumeSource
Binding = io__k8s__api__core__v1__Binding
CSIPersistentVolumeSource = io__k8s__api__core__v1__CSIPersistentVolumeSource
CSIVolumeSource = io__k8s__api__core__v1__CSIVolumeSource
Capabilities = io__k8s__api__core__v1__Capabilities
CephFSPersistentVolumeSource = io__k8s__api__core__v1__CephFSPersistentVolumeSource
CephFSVolumeSource = io__k8s__api__core__v1__CephFSVolumeSource
CinderPersistentVolumeSource = io__k8s__api__core__v1__CinderPersistentVolumeSource
CinderVolumeSource = io__k8s__api__core__v1__CinderVolumeSource
ClientIPConfig = io__k8s__api__core__v1__ClientIPConfig
ComponentCondition = io__k8s__api__core__v1__ComponentCondition
ComponentStatus = io__k8s__api__core__v1__ComponentStatus
ComponentStatusList = io__k8s__api__core__v1__ComponentStatusList
ConfigMap = io__k8s__api__core__v1__ConfigMap
ConfigMapEnvSource = io__k8s__api__core__v1__ConfigMapEnvSource
ConfigMapKeySelector = io__k8s__api__core__v1__ConfigMapKeySelector
ConfigMapList = io__k8s__api__core__v1__ConfigMapList
ConfigMapNodeConfigSource = io__k8s__api__core__v1__ConfigMapNodeConfigSource
ConfigMapProjection = io__k8s__api__core__v1__ConfigMapProjection
ConfigMapVolumeSource = io__k8s__api__core__v1__ConfigMapVolumeSource
Container = io__k8s__api__core__v1__Container
ContainerImage = io__k8s__api__core__v1__ContainerImage
ContainerPort = io__k8s__api__core__v1__ContainerPort
ContainerState = io__k8s__api__core__v1__ContainerState
ContainerStateRunning = io__k8s__api__core__v1__ContainerStateRunning
ContainerStateTerminated = io__k8s__api__core__v1__ContainerStateTerminated
ContainerStateWaiting = io__k8s__api__core__v1__ContainerStateWaiting
ContainerStatus = io__k8s__api__core__v1__ContainerStatus
DaemonEndpoint = io__k8s__api__core__v1__DaemonEndpoint
DownwardAPIProjection = io__k8s__api__core__v1__DownwardAPIProjection
DownwardAPIVolumeFile = io__k8s__api__core__v1__DownwardAPIVolumeFile
DownwardAPIVolumeSource = io__k8s__api__core__v1__DownwardAPIVolumeSource
EmptyDirVolumeSource = io__k8s__api__core__v1__EmptyDirVolumeSource
EndpointAddress = io__k8s__api__core__v1__EndpointAddress
EndpointPort = io__k8s__api__discovery__v1beta1__EndpointPort
EndpointSubset = io__k8s__api__core__v1__EndpointSubset
Endpoints = io__k8s__api__core__v1__Endpoints
EndpointsList = io__k8s__api__core__v1__EndpointsList
EnvFromSource = io__k8s__api__core__v1__EnvFromSource
EnvVar = io__k8s__api__core__v1__EnvVar
EnvVarSource = io__k8s__api__core__v1__EnvVarSource
EphemeralContainer = io__k8s__api__core__v1__EphemeralContainer
EphemeralVolumeSource = io__k8s__api__core__v1__EphemeralVolumeSource
Event = io__k8s__api__core__v1__Event
EventList = io__k8s__api__core__v1__EventList
EventSeries = io__k8s__api__events__v1beta1__EventSeries
EventSource = io__k8s__api__core__v1__EventSource
ExecAction = io__k8s__api__core__v1__ExecAction
FCVolumeSource = io__k8s__api__core__v1__FCVolumeSource
FlexPersistentVolumeSource = io__k8s__api__core__v1__FlexPersistentVolumeSource
FlexVolumeSource = io__k8s__api__core__v1__FlexVolumeSource
FlockerVolumeSource = io__k8s__api__core__v1__FlockerVolumeSource
GCEPersistentDiskVolumeSource = io__k8s__api__core__v1__GCEPersistentDiskVolumeSource
GRPCAction = io__k8s__api__core__v1__GRPCAction
GitRepoVolumeSource = io__k8s__api__core__v1__GitRepoVolumeSource
GlusterfsPersistentVolumeSource = (
    io__k8s__api__core__v1__GlusterfsPersistentVolumeSource
)
GlusterfsVolumeSource = io__k8s__api__core__v1__GlusterfsVolumeSource
HTTPGetAction = io__k8s__api__core__v1__HTTPGetAction
HTTPHeader = io__k8s__api__core__v1__HTTPHeader
HostAlias = io__k8s__api__core__v1__HostAlias
HostPathVolumeSource = io__k8s__api__core__v1__HostPathVolumeSource
ISCSIPersistentVolumeSource = io__k8s__api__core__v1__ISCSIPersistentVolumeSource
ISCSIVolumeSource = io__k8s__api__core__v1__ISCSIVolumeSource
KeyToPath = io__k8s__api__core__v1__KeyToPath
Lifecycle = io__k8s__api__core__v1__Lifecycle
LifecycleHandler = io__k8s__api__core__v1__LifecycleHandler
LimitRange = io__k8s__api__core__v1__LimitRange
LimitRangeItem = io__k8s__api__core__v1__LimitRangeItem
LimitRangeList = io__k8s__api__core__v1__LimitRangeList
LimitRangeSpec = io__k8s__api__core__v1__LimitRangeSpec
LoadBalancerIngress = io__k8s__api__core__v1__LoadBalancerIngress
LoadBalancerStatus = io__k8s__api__core__v1__LoadBalancerStatus
LocalObjectReference = io__k8s__api__core__v1__LocalObjectReference
LocalVolumeSource = io__k8s__api__core__v1__LocalVolumeSource
NFSVolumeSource = io__k8s__api__core__v1__NFSVolumeSource
Namespace = io__k8s__api__core__v1__Namespace
NamespaceCondition = io__k8s__api__core__v1__NamespaceCondition
NamespaceList = io__k8s__api__core__v1__NamespaceList
NamespaceSpec = io__k8s__api__core__v1__NamespaceSpec
NamespaceStatus = io__k8s__api__core__v1__NamespaceStatus
Node = io__k8s__api__core__v1__Node
NodeAddress = io__k8s__api__core__v1__NodeAddress
NodeAffinity = io__k8s__api__core__v1__NodeAffinity
NodeCondition = io__k8s__api__core__v1__NodeCondition
NodeConfigSource = io__k8s__api__core__v1__NodeConfigSource
NodeConfigStatus = io__k8s__api__core__v1__NodeConfigStatus
NodeDaemonEndpoints = io__k8s__api__core__v1__NodeDaemonEndpoints
NodeList = io__k8s__api__core__v1__NodeList
NodeSelector = io__k8s__api__core__v1__NodeSelector
NodeSelectorRequirement = io__k8s__api__core__v1__NodeSelectorRequirement
NodeSelectorTerm = io__k8s__api__core__v1__NodeSelectorTerm
NodeSpec = io__k8s__api__core__v1__NodeSpec
NodeStatus = io__k8s__api__core__v1__NodeStatus
NodeSystemInfo = io__k8s__api__core__v1__NodeSystemInfo
ObjectFieldSelector = io__k8s__api__core__v1__ObjectFieldSelector
ObjectReference = io__k8s__api__core__v1__ObjectReference
PersistentVolume = io__k8s__api__core__v1__PersistentVolume
PersistentVolumeClaim = io__k8s__api__core__v1__PersistentVolumeClaim
PersistentVolumeClaimCondition = io__k8s__api__core__v1__PersistentVolumeClaimCondition
PersistentVolumeClaimList = io__k8s__api__core__v1__PersistentVolumeClaimList
PersistentVolumeClaimSpec = io__k8s__api__core__v1__PersistentVolumeClaimSpec
PersistentVolumeClaimStatus = io__k8s__api__core__v1__PersistentVolumeClaimStatus
PersistentVolumeClaimTemplate = io__k8s__api__core__v1__PersistentVolumeClaimTemplate
PersistentVolumeClaimVolumeSource = (
    io__k8s__api__core__v1__PersistentVolumeClaimVolumeSource
)
PersistentVolumeList = io__k8s__api__core__v1__PersistentVolumeList
PersistentVolumeSpec = io__k8s__api__core__v1__PersistentVolumeSpec
PersistentVolumeStatus = io__k8s__api__core__v1__PersistentVolumeStatus
PhotonPersistentDiskVolumeSource = (
    io__k8s__api__core__v1__PhotonPersistentDiskVolumeSource
)
Pod = io__k8s__api__core__v1__Pod
PodAffinity = io__k8s__api__core__v1__PodAffinity
PodAffinityTerm = io__k8s__api__core__v1__PodAffinityTerm
PodAntiAffinity = io__k8s__api__core__v1__PodAntiAffinity
PodCondition = io__k8s__api__core__v1__PodCondition
PodDNSConfig = io__k8s__api__core__v1__PodDNSConfig
PodDNSConfigOption = io__k8s__api__core__v1__PodDNSConfigOption
PodIP = io__k8s__api__core__v1__PodIP
PodList = io__k8s__api__core__v1__PodList
PodOS = io__k8s__api__core__v1__PodOS
PodReadinessGate = io__k8s__api__core__v1__PodReadinessGate
PodSecurityContext = io__k8s__api__core__v1__PodSecurityContext
PodSpec = io__k8s__api__core__v1__PodSpec
PodStatus = io__k8s__api__core__v1__PodStatus
PodTemplate = io__k8s__api__core__v1__PodTemplate
PodTemplateList = io__k8s__api__core__v1__PodTemplateList
PodTemplateSpec = io__k8s__api__core__v1__PodTemplateSpec
PortStatus = io__k8s__api__core__v1__PortStatus
PortworxVolumeSource = io__k8s__api__core__v1__PortworxVolumeSource
PreferredSchedulingTerm = io__k8s__api__core__v1__PreferredSchedulingTerm
Probe = io__k8s__api__core__v1__Probe
ProjectedVolumeSource = io__k8s__api__core__v1__ProjectedVolumeSource
QuobyteVolumeSource = io__k8s__api__core__v1__QuobyteVolumeSource
RBDPersistentVolumeSource = io__k8s__api__core__v1__RBDPersistentVolumeSource
RBDVolumeSource = io__k8s__api__core__v1__RBDVolumeSource
ReplicationController = io__k8s__api__core__v1__ReplicationController
ReplicationControllerCondition = io__k8s__api__core__v1__ReplicationControllerCondition
ReplicationControllerList = io__k8s__api__core__v1__ReplicationControllerList
ReplicationControllerSpec = io__k8s__api__core__v1__ReplicationControllerSpec
ReplicationControllerStatus = io__k8s__api__core__v1__ReplicationControllerStatus
ResourceFieldSelector = io__k8s__api__core__v1__ResourceFieldSelector
ResourceQuota = io__k8s__api__core__v1__ResourceQuota
ResourceQuotaList = io__k8s__api__core__v1__ResourceQuotaList
ResourceQuotaSpec = io__k8s__api__core__v1__ResourceQuotaSpec
ResourceQuotaStatus = io__k8s__api__core__v1__ResourceQuotaStatus
ResourceRequirements = io__k8s__api__core__v1__ResourceRequirements
SELinuxOptions = io__k8s__api__core__v1__SELinuxOptions
ScaleIOPersistentVolumeSource = io__k8s__api__core__v1__ScaleIOPersistentVolumeSource
ScaleIOVolumeSource = io__k8s__api__core__v1__ScaleIOVolumeSource
ScopeSelector = io__k8s__api__core__v1__ScopeSelector
ScopedResourceSelectorRequirement = (
    io__k8s__api__core__v1__ScopedResourceSelectorRequirement
)
SeccompProfile = io__k8s__api__core__v1__SeccompProfile
Secret = io__k8s__api__core__v1__Secret
SecretEnvSource = io__k8s__api__core__v1__SecretEnvSource
SecretKeySelector = io__k8s__api__core__v1__SecretKeySelector
SecretList = io__k8s__api__core__v1__SecretList
SecretProjection = io__k8s__api__core__v1__SecretProjection
SecretReference = io__k8s__api__core__v1__SecretReference
SecretVolumeSource = io__k8s__api__core__v1__SecretVolumeSource
SecurityContext = io__k8s__api__core__v1__SecurityContext
Service = io__k8s__api__core__v1__Service
ServiceAccount = io__k8s__api__core__v1__ServiceAccount
ServiceAccountList = io__k8s__api__core__v1__ServiceAccountList
ServiceAccountTokenProjection = io__k8s__api__core__v1__ServiceAccountTokenProjection
ServiceList = io__k8s__api__core__v1__ServiceList
ServicePort = io__k8s__api__core__v1__ServicePort
ServiceSpec = io__k8s__api__core__v1__ServiceSpec
ServiceStatus = io__k8s__api__core__v1__ServiceStatus
SessionAffinityConfig = io__k8s__api__core__v1__SessionAffinityConfig
StorageOSPersistentVolumeSource = (
    io__k8s__api__core__v1__StorageOSPersistentVolumeSource
)
StorageOSVolumeSource = io__k8s__api__core__v1__StorageOSVolumeSource
Sysctl = io__k8s__api__core__v1__Sysctl
TCPSocketAction = io__k8s__api__core__v1__TCPSocketAction
Taint = io__k8s__api__core__v1__Taint
Toleration = io__k8s__api__core__v1__Toleration
TopologySelectorLabelRequirement = (
    io__k8s__api__core__v1__TopologySelectorLabelRequirement
)
TopologySelectorTerm = io__k8s__api__core__v1__TopologySelectorTerm
TopologySpreadConstraint = io__k8s__api__core__v1__TopologySpreadConstraint
TypedLocalObjectReference = io__k8s__api__core__v1__TypedLocalObjectReference
Volume = io__k8s__api__core__v1__Volume
VolumeDevice = io__k8s__api__core__v1__VolumeDevice
VolumeMount = io__k8s__api__core__v1__VolumeMount
VolumeNodeAffinity = io__k8s__api__core__v1__VolumeNodeAffinity
VolumeProjection = io__k8s__api__core__v1__VolumeProjection
VsphereVirtualDiskVolumeSource = io__k8s__api__core__v1__VsphereVirtualDiskVolumeSource
WeightedPodAffinityTerm = io__k8s__api__core__v1__WeightedPodAffinityTerm
WindowsSecurityContextOptions = io__k8s__api__core__v1__WindowsSecurityContextOptions
Endpoint = io__k8s__api__discovery__v1beta1__Endpoint
EndpointConditions = io__k8s__api__discovery__v1beta1__EndpointConditions
EndpointHints = io__k8s__api__discovery__v1beta1__EndpointHints
EndpointSlice = io__k8s__api__discovery__v1__EndpointSlice
EndpointSliceList = io__k8s__api__discovery__v1__EndpointSliceList
ForZone = io__k8s__api__discovery__v1beta1__ForZone
discovery__k8s__io_v1beta1_EndpointSlice = (
    io__k8s__api__discovery__v1beta1__EndpointSlice
)
discovery__k8s__io_v1beta1_EndpointSliceList = (
    io__k8s__api__discovery__v1beta1__EndpointSliceList
)
events__k8s__io_v1_Event = io__k8s__api__events__v1__Event
events__k8s__io_v1_EventList = io__k8s__api__events__v1__EventList
events__k8s__io_v1beta1_Event = io__k8s__api__events__v1beta1__Event
events__k8s__io_v1beta1_EventList = io__k8s__api__events__v1beta1__EventList
FlowDistinguisherMethod = io__k8s__api__flowcontrol__v1beta2__FlowDistinguisherMethod
FlowSchema = io__k8s__api__flowcontrol__v1beta1__FlowSchema
FlowSchemaCondition = io__k8s__api__flowcontrol__v1beta2__FlowSchemaCondition
FlowSchemaList = io__k8s__api__flowcontrol__v1beta1__FlowSchemaList
FlowSchemaSpec = io__k8s__api__flowcontrol__v1beta2__FlowSchemaSpec
FlowSchemaStatus = io__k8s__api__flowcontrol__v1beta2__FlowSchemaStatus
GroupSubject = io__k8s__api__flowcontrol__v1beta2__GroupSubject
LimitResponse = io__k8s__api__flowcontrol__v1beta2__LimitResponse
LimitedPriorityLevelConfiguration = (
    io__k8s__api__flowcontrol__v1beta2__LimitedPriorityLevelConfiguration
)
NonResourcePolicyRule = io__k8s__api__flowcontrol__v1beta2__NonResourcePolicyRule
PolicyRulesWithSubjects = io__k8s__api__flowcontrol__v1beta2__PolicyRulesWithSubjects
PriorityLevelConfiguration = (
    io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfiguration
)
PriorityLevelConfigurationCondition = (
    io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationCondition
)
PriorityLevelConfigurationList = (
    io__k8s__api__flowcontrol__v1beta1__PriorityLevelConfigurationList
)
PriorityLevelConfigurationReference = (
    io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationReference
)
PriorityLevelConfigurationSpec = (
    io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationSpec
)
PriorityLevelConfigurationStatus = (
    io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationStatus
)
QueuingConfiguration = io__k8s__api__flowcontrol__v1beta2__QueuingConfiguration
ResourcePolicyRule = io__k8s__api__flowcontrol__v1beta2__ResourcePolicyRule
ServiceAccountSubject = io__k8s__api__flowcontrol__v1beta2__ServiceAccountSubject
Subject = io__k8s__api__rbac__v1__Subject
UserSubject = io__k8s__api__flowcontrol__v1beta2__UserSubject
flowcontrol__apiserver__k8s__io_v1beta2_FlowSchema = (
    io__k8s__api__flowcontrol__v1beta2__FlowSchema
)
flowcontrol__apiserver__k8s__io_v1beta2_FlowSchemaList = (
    io__k8s__api__flowcontrol__v1beta2__FlowSchemaList
)
flowcontrol__apiserver__k8s__io_v1beta2_PriorityLevelConfiguration = (
    io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfiguration
)
flowcontrol__apiserver__k8s__io_v1beta2_PriorityLevelConfigurationList = (
    io__k8s__api__flowcontrol__v1beta2__PriorityLevelConfigurationList
)
HTTPIngressPath = io__k8s__api__networking__v1__HTTPIngressPath
HTTPIngressRuleValue = io__k8s__api__networking__v1__HTTPIngressRuleValue
IPBlock = io__k8s__api__networking__v1__IPBlock
Ingress = io__k8s__api__networking__v1__Ingress
IngressBackend = io__k8s__api__networking__v1__IngressBackend
IngressClass = io__k8s__api__networking__v1__IngressClass
IngressClassList = io__k8s__api__networking__v1__IngressClassList
IngressClassParametersReference = (
    io__k8s__api__networking__v1__IngressClassParametersReference
)
IngressClassSpec = io__k8s__api__networking__v1__IngressClassSpec
IngressList = io__k8s__api__networking__v1__IngressList
IngressRule = io__k8s__api__networking__v1__IngressRule
IngressServiceBackend = io__k8s__api__networking__v1__IngressServiceBackend
IngressSpec = io__k8s__api__networking__v1__IngressSpec
IngressStatus = io__k8s__api__networking__v1__IngressStatus
IngressTLS = io__k8s__api__networking__v1__IngressTLS
NetworkPolicy = io__k8s__api__networking__v1__NetworkPolicy
NetworkPolicyEgressRule = io__k8s__api__networking__v1__NetworkPolicyEgressRule
NetworkPolicyIngressRule = io__k8s__api__networking__v1__NetworkPolicyIngressRule
NetworkPolicyList = io__k8s__api__networking__v1__NetworkPolicyList
NetworkPolicyPeer = io__k8s__api__networking__v1__NetworkPolicyPeer
NetworkPolicyPort = io__k8s__api__networking__v1__NetworkPolicyPort
NetworkPolicySpec = io__k8s__api__networking__v1__NetworkPolicySpec
ServiceBackendPort = io__k8s__api__networking__v1__ServiceBackendPort
Overhead = io__k8s__api__node__v1beta1__Overhead
RuntimeClass = io__k8s__api__node__v1__RuntimeClass
RuntimeClassList = io__k8s__api__node__v1__RuntimeClassList
Scheduling = io__k8s__api__node__v1beta1__Scheduling
node__k8s__io_v1beta1_RuntimeClass = io__k8s__api__node__v1beta1__RuntimeClass
node__k8s__io_v1beta1_RuntimeClassList = io__k8s__api__node__v1beta1__RuntimeClassList
Eviction = io__k8s__api__policy__v1__Eviction
PodDisruptionBudget = io__k8s__api__policy__v1__PodDisruptionBudget
PodDisruptionBudgetList = io__k8s__api__policy__v1__PodDisruptionBudgetList
PodDisruptionBudgetSpec = io__k8s__api__policy__v1beta1__PodDisruptionBudgetSpec
PodDisruptionBudgetStatus = io__k8s__api__policy__v1beta1__PodDisruptionBudgetStatus
AllowedCSIDriver = io__k8s__api__policy__v1beta1__AllowedCSIDriver
AllowedFlexVolume = io__k8s__api__policy__v1beta1__AllowedFlexVolume
AllowedHostPath = io__k8s__api__policy__v1beta1__AllowedHostPath
FSGroupStrategyOptions = io__k8s__api__policy__v1beta1__FSGroupStrategyOptions
HostPortRange = io__k8s__api__policy__v1beta1__HostPortRange
IDRange = io__k8s__api__policy__v1beta1__IDRange
policy_v1beta1_PodDisruptionBudget = io__k8s__api__policy__v1beta1__PodDisruptionBudget
policy_v1beta1_PodDisruptionBudgetList = (
    io__k8s__api__policy__v1beta1__PodDisruptionBudgetList
)
PodSecurityPolicy = io__k8s__api__policy__v1beta1__PodSecurityPolicy
PodSecurityPolicyList = io__k8s__api__policy__v1beta1__PodSecurityPolicyList
PodSecurityPolicySpec = io__k8s__api__policy__v1beta1__PodSecurityPolicySpec
RunAsGroupStrategyOptions = io__k8s__api__policy__v1beta1__RunAsGroupStrategyOptions
RunAsUserStrategyOptions = io__k8s__api__policy__v1beta1__RunAsUserStrategyOptions
RuntimeClassStrategyOptions = io__k8s__api__policy__v1beta1__RuntimeClassStrategyOptions
SELinuxStrategyOptions = io__k8s__api__policy__v1beta1__SELinuxStrategyOptions
SupplementalGroupsStrategyOptions = (
    io__k8s__api__policy__v1beta1__SupplementalGroupsStrategyOptions
)
AggregationRule = io__k8s__api__rbac__v1__AggregationRule
ClusterRole = io__k8s__api__rbac__v1__ClusterRole
ClusterRoleBinding = io__k8s__api__rbac__v1__ClusterRoleBinding
ClusterRoleBindingList = io__k8s__api__rbac__v1__ClusterRoleBindingList
ClusterRoleList = io__k8s__api__rbac__v1__ClusterRoleList
PolicyRule = io__k8s__api__rbac__v1__PolicyRule
Role = io__k8s__api__rbac__v1__Role
RoleBinding = io__k8s__api__rbac__v1__RoleBinding
RoleBindingList = io__k8s__api__rbac__v1__RoleBindingList
RoleList = io__k8s__api__rbac__v1__RoleList
RoleRef = io__k8s__api__rbac__v1__RoleRef
PriorityClass = io__k8s__api__scheduling__v1__PriorityClass
PriorityClassList = io__k8s__api__scheduling__v1__PriorityClassList
CSIDriver = io__k8s__api__storage__v1__CSIDriver
CSIDriverList = io__k8s__api__storage__v1__CSIDriverList
CSIDriverSpec = io__k8s__api__storage__v1__CSIDriverSpec
CSINode = io__k8s__api__storage__v1__CSINode
CSINodeDriver = io__k8s__api__storage__v1__CSINodeDriver
CSINodeList = io__k8s__api__storage__v1__CSINodeList
CSINodeSpec = io__k8s__api__storage__v1__CSINodeSpec
CSIStorageCapacity = io__k8s__api__storage__v1__CSIStorageCapacity
CSIStorageCapacityList = io__k8s__api__storage__v1__CSIStorageCapacityList
StorageClass = io__k8s__api__storage__v1__StorageClass
StorageClassList = io__k8s__api__storage__v1__StorageClassList
VolumeAttachment = io__k8s__api__storage__v1__VolumeAttachment
VolumeAttachmentList = io__k8s__api__storage__v1__VolumeAttachmentList
VolumeAttachmentSource = io__k8s__api__storage__v1__VolumeAttachmentSource
VolumeAttachmentSpec = io__k8s__api__storage__v1__VolumeAttachmentSpec
VolumeAttachmentStatus = io__k8s__api__storage__v1__VolumeAttachmentStatus
VolumeError = io__k8s__api__storage__v1__VolumeError
VolumeNodeResources = io__k8s__api__storage__v1__VolumeNodeResources
storage__k8s__io_v1alpha1_CSIStorageCapacity = (
    io__k8s__api__storage__v1alpha1__CSIStorageCapacity
)
storage__k8s__io_v1alpha1_CSIStorageCapacityList = (
    io__k8s__api__storage__v1alpha1__CSIStorageCapacityList
)
storage__k8s__io_v1beta1_CSIStorageCapacity = (
    io__k8s__api__storage__v1beta1__CSIStorageCapacity
)
storage__k8s__io_v1beta1_CSIStorageCapacityList = (
    io__k8s__api__storage__v1beta1__CSIStorageCapacityList
)
CustomResourceColumnDefinition = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceColumnDefinition
CustomResourceConversion = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceConversion
CustomResourceDefinition = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinition
CustomResourceDefinitionCondition = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionCondition
CustomResourceDefinitionList = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionList
CustomResourceDefinitionNames = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionNames
CustomResourceDefinitionSpec = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionSpec
CustomResourceDefinitionStatus = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionStatus
CustomResourceDefinitionVersion = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceDefinitionVersion
CustomResourceSubresourceScale = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresourceScale
CustomResourceSubresourceStatus = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresourceStatus
CustomResourceSubresources = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceSubresources
CustomResourceValidation = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__CustomResourceValidation
ExternalDocumentation = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ExternalDocumentation
JSON = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSON
JSONSchemaProps = (
    io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaProps
)
JSONSchemaPropsOrArray = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrArray
JSONSchemaPropsOrBool = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrBool
JSONSchemaPropsOrStringArray = io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__JSONSchemaPropsOrStringArray
ValidationRule = (
    io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__ValidationRule
)
WebhookConversion = (
    io__k8s__apiextensions_apiserver__pkg__apis__apiextensions__v1__WebhookConversion
)
APIGroup = io__k8s__apimachinery__pkg__apis__meta__v1__APIGroup
APIGroupList = io__k8s__apimachinery__pkg__apis__meta__v1__APIGroupList
APIResource = io__k8s__apimachinery__pkg__apis__meta__v1__APIResource
APIResourceList = io__k8s__apimachinery__pkg__apis__meta__v1__APIResourceList
APIVersions = io__k8s__apimachinery__pkg__apis__meta__v1__APIVersions
Condition = io__k8s__apimachinery__pkg__apis__meta__v1__Condition
DeleteOptions = io__k8s__apimachinery__pkg__apis__meta__v1__DeleteOptions
FieldsV1 = io__k8s__apimachinery__pkg__apis__meta__v1__FieldsV1
GroupVersionForDiscovery = (
    io__k8s__apimachinery__pkg__apis__meta__v1__GroupVersionForDiscovery
)
LabelSelector = io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelector
LabelSelectorRequirement = (
    io__k8s__apimachinery__pkg__apis__meta__v1__LabelSelectorRequirement
)
ListMeta = io__k8s__apimachinery__pkg__apis__meta__v1__ListMeta
ManagedFieldsEntry = io__k8s__apimachinery__pkg__apis__meta__v1__ManagedFieldsEntry
ObjectMeta = io__k8s__apimachinery__pkg__apis__meta__v1__ObjectMeta
OwnerReference = io__k8s__apimachinery__pkg__apis__meta__v1__OwnerReference
Patch = io__k8s__apimachinery__pkg__apis__meta__v1__Patch
Preconditions = io__k8s__apimachinery__pkg__apis__meta__v1__Preconditions
ServerAddressByClientCIDR = (
    io__k8s__apimachinery__pkg__apis__meta__v1__ServerAddressByClientCIDR
)
Status = io__k8s__apimachinery__pkg__apis__meta__v1__Status
StatusCause = io__k8s__apimachinery__pkg__apis__meta__v1__StatusCause
StatusDetails = io__k8s__apimachinery__pkg__apis__meta__v1__StatusDetails
WatchEvent = io__k8s__apimachinery__pkg__apis__meta__v1__WatchEvent
RawExtension = io__k8s__apimachinery__pkg__runtime__RawExtension
Info = io__k8s__apimachinery__pkg__version__Info
APIService = io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIService
APIServiceCondition = (
    io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceCondition
)
APIServiceList = (
    io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceList
)
APIServiceSpec = (
    io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceSpec
)
APIServiceStatus = (
    io__k8s__kube_aggregator__pkg__apis__apiregistration__v1__APIServiceStatus
)
