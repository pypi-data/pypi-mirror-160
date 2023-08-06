"use strict";
(self["webpackChunkglobus_jupyterlab"] = self["webpackChunkglobus_jupyterlab"] || []).push([["lib_index_js"],{

/***/ "./lib/components/Endpoint.js":
/*!************************************!*\
  !*** ./lib/components/Endpoint.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! recoil */ "webpack/sharing/consume/default/recoil/recoil");
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(recoil__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _GlobusObjects__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./GlobusObjects */ "./lib/components/GlobusObjects.js");
/* harmony import */ var _HubLoginWidget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./HubLoginWidget */ "./lib/components/HubLoginWidget.js");
/* harmony import */ var path__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! path */ "./node_modules/path-browserify/index.js");
/* harmony import */ var path__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(path__WEBPACK_IMPORTED_MODULE_3__);








var _path = path__WEBPACK_IMPORTED_MODULE_3__;
const useQuery = () => {
    const { search } = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_0__.useLocation)();
    return react__WEBPACK_IMPORTED_MODULE_1___default().useMemo(() => new URLSearchParams(search), [search]);
};
const Endpoint = (props) => {
    // Local State
    const [apiError, setAPIError] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    const [endpointList, setEndpointList] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({ DATA: [], path: null });
    const [endpoint, setEndpoint] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    const [hubResponse, setHubResponse] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [selectedEndpointItems, setSelectedEndpointItems] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)([]);
    const [transfer, setTransfer] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    const itemsRef = react__WEBPACK_IMPORTED_MODULE_1___default().useRef([]);
    const [lastChecked, setLastChecked] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    const [shift, setShift] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    // Recoil (global) State
    const config = (0,recoil__WEBPACK_IMPORTED_MODULE_2__.useRecoilValue)(_GlobusObjects__WEBPACK_IMPORTED_MODULE_4__.ConfigAtom);
    // React Router history and params
    let history = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_0__.useHistory)();
    let params = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_0__.useParams)();
    let endpointID = params.endpointID;
    let path = params.path;
    let query = useQuery();
    // ComponentDidMount Functions
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        const handleKeyUp = (event) => {
            if (event.shiftKey) {
                setShift(false);
            }
        };
        document.addEventListener("keyup", handleKeyUp);
        return () => {
            document.removeEventListener("keyup", handleKeyUp);
        };
    }, []);
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        const handleKeyDown = (event) => {
            if (event.shiftKey) {
                setShift(true);
            }
        };
        document.addEventListener("keydown", handleKeyDown);
        return () => {
            document.removeEventListener("keydown", handleKeyDown);
        };
    }, []);
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        listEndpointItems(endpointID, path);
        return () => {
            setAPIError(null);
            setEndpointList({ DATA: [], path: null });
        };
    }, [endpointID, path]);
    // @ts-ignore
    const getSelectedFiles = () => {
        const selectedFiles = props.factory.tracker.currentWidget.selectedItems();
        let jupyterItems = [], fileCheck = true;
        while (fileCheck) {
            let file = selectedFiles.next();
            if (file) {
                jupyterItems.push(file);
            }
            else {
                fileCheck = false;
            }
        }
        return jupyterItems;
    };
    const listEndpointItems = async (endpointID, path = null) => {
        setLoading(true);
        setAPIError(null);
        setEndpointList({ DATA: [], path: null });
        let endpoint = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)(`endpoint_detail?endpoint=${endpointID}`);
        if (!endpoint["activated"] && endpoint["expires_in"] == 0) {
            let activated = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("endpoint_autoactivate", {
                body: JSON.stringify({ endpoint_id: endpoint["id"] }),
                method: "POST",
            });
            // Need to research if there is anything meaningful to do with the activation result
            console.log(activated);
        }
        setEndpoint(endpoint);
        try {
            var fullPath = query.get("full-path");
            var url = `operation_ls?endpoint=${endpointID}`;
            if (fullPath) {
                url = `${url}&path=${fullPath}`;
            }
            const listItems = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)(url);
            setLoading(false);
            setEndpointList(listItems);
        }
        catch (error) {
            setLoading(false);
            setAPIError(Object.assign(Object.assign({}, error), { global: true }));
            let error_response = await error.response.json();
            /*
              Note: This probably isn't a great UX to simply pop up a login page, but it
              does demonstrate the base functionality for picking endpoints
            */
            if ("login_url" in error_response) {
                // Poll for successful authentication.
                var lastConfig = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("config");
                var lastLogin = new Date(lastConfig.last_login).getTime();
                let authInterval = window.setInterval(async () => {
                    const updatedConfig = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("config");
                    var newLogin = new Date(updatedConfig.last_login).getTime();
                    if (newLogin !== lastLogin) {
                        history.push("/");
                        history.replace(`/endpoints/${endpointID}`);
                        clearInterval(authInterval);
                    }
                }, 1000);
                if (config.is_hub) {
                    setAPIError(null);
                    setHubResponse(error_response);
                }
                else {
                    window
                        .open(error_response.login_url, "Globus Login", "height=600,width=800")
                        .focus();
                }
            }
        }
        setLoading(false);
    };
    // Event Handlers
    const handleEndpointSelect = (event) => {
        var checked;
        if (shift) {
            if (lastChecked !== null) {
                let checkboxes = itemsRef.current;
                let start = checkboxes.indexOf(lastChecked);
                let end = checkboxes.indexOf(event.target);
                checked = checkboxes.slice(Math.min(start, end), Math.max(start, end) + 1);
                checked.forEach((el) => {
                    el.checked = start < end ? true : false;
                });
            }
        }
        else {
            checked = [event.target];
        }
        // Only need unique values from checked
        checked = [...new Set(checked)];
        // Reset selectedEndpointItems if checked items length > 1
        if (checked.length > 1) {
            setSelectedEndpointItems([]);
        }
        // Build selectedEndpointItems
        checked.forEach((el, index) => {
            if (el.checked) {
                setSelectedEndpointItems((selectedEndpointItems) => {
                    return [JSON.parse(el.value), ...selectedEndpointItems];
                });
            }
            else {
                const removeItem = JSON.parse(el.value);
                const index = selectedEndpointItems
                    .map((item) => {
                    return item.name;
                })
                    .indexOf(removeItem.name);
                if (index > -1) {
                    selectedEndpointItems.splice(index, 1);
                    setSelectedEndpointItems(selectedEndpointItems);
                }
            }
        });
        setLastChecked(event.target);
    };
    const handleTransferToJupyter = async (event) => {
        event.preventDefault();
        setAPIError(null);
        setLoading(true);
        setTransfer(null);
        var destinationEndpoint = config.collection_id;
        var sourceEndpoint = endpoint.id;
        var transferItems = [];
        if (props.selectedJupyterItems.directories.length === 0 ||
            props.selectedJupyterItems.directories.length > 1) {
            setLoading(false);
            setAPIError({
                response: {
                    status: "DirectorySelectionError",
                    statusText: "To transfer to Jupyter Hub, you must select only one directory to transfer to.",
                },
            });
        }
        else {
            // Loop through selectedEndpointItems from state
            for (let selectedEndpointItem of selectedEndpointItems) {
                let sourcePath = _path.posix.resolve(endpointList.path, selectedEndpointItem.name);
                let destinationPath = _path.posix.resolve(config.collection_base_path, props.selectedJupyterItems.directories[0].path, selectedEndpointItem.name);
                transferItems.push({
                    source_path: sourcePath,
                    destination_path: destinationPath,
                    recursive: selectedEndpointItem.type == "dir" ? true : false,
                });
            }
            let transferRequest = {
                source_endpoint: sourceEndpoint,
                destination_endpoint: destinationEndpoint,
                DATA: transferItems,
            };
            try {
                const transferResponse = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("submit_transfer", {
                    body: JSON.stringify(transferRequest),
                    method: "POST",
                });
                setLoading(false);
                setTransfer(transferResponse);
            }
            catch (error) {
                setLoading(false);
                setAPIError(error);
            }
        }
    };
    const handleTransferFromJupyter = async (event) => {
        event.preventDefault();
        setAPIError(null);
        setLoading(true);
        setTransfer(null);
        var destinationEndpoint = endpoint.id;
        var sourceEndpoint = config.collection_id;
        var transferItems = [];
        if (selectedEndpointItems.length > 1) {
            setAPIError({
                response: {
                    status: "DirectorySelectionError",
                    statusText: "Please only select one remote directory to transfer data to",
                },
            });
        }
        // Loop through selectedJupyterItems from props
        if (props.selectedJupyterItems.directories.length) {
            for (let directory of props.selectedJupyterItems.directories) {
                let destinationPath = selectedEndpointItems.length
                    ? _path.posix.resolve(endpointList.path, selectedEndpointItems[0].name, directory.path)
                    : _path.posix.resolve(endpointList.path, directory.path);
                let sourcePath = _path.posix.resolve(config.collection_base_path, directory.path);
                transferItems.push({
                    source_path: sourcePath,
                    destination_path: destinationPath,
                    recursive: true,
                });
            }
        }
        if (props.selectedJupyterItems.files.length) {
            for (let file of props.selectedJupyterItems.files) {
                let destinationPath = selectedEndpointItems.length
                    ? _path.posix.resolve(endpointList.path, selectedEndpointItems[0].name, file.path)
                    : _path.posix.resolve(endpointList.path, file.path);
                let sourcePath = _path.posix.resolve(config.collection_base_path, file.path);
                transferItems.push({
                    source_path: sourcePath,
                    destination_path: destinationPath,
                    recursive: false,
                });
            }
        }
        let transferRequest = {
            source_endpoint: sourceEndpoint,
            destination_endpoint: destinationEndpoint,
            DATA: transferItems,
        };
        try {
            const transferResponse = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("submit_transfer", {
                body: JSON.stringify(transferRequest),
                method: "POST",
            });
            setLoading(false);
            setTransfer(transferResponse);
        }
        catch (error) {
            setLoading(false);
            setAPIError(error);
            console.log(error);
        }
    };
    if (apiError && apiError.global) {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "alert alert-danger alert-dismissible col-8 fade show" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("strong", null,
                "Error ",
                apiError.response.status,
                ": ",
                apiError.response.error,
                "."),
            " ",
            apiError.details && apiError.details,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { type: "button", className: "btn-close", "data-bs-dismiss": "alert", "aria-label": "Close" })));
    }
    if (loading) {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h5", { className: "mt-3" }, "Loading");
    }
    if (hubResponse) {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_HubLoginWidget__WEBPACK_IMPORTED_MODULE_6__.HubLogin, { endpoint: endpoint, hubResponse: hubResponse });
    }
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null, endpointList["DATA"].length > 0 ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "mt-3" },
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h5", null,
            "Browsing Collection ",
            endpoint ? endpoint.display_name : endpointID),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "btn-group mb-4 mt-2" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: "btn btn-sm btn-outline-primary", onClick: () => history.goBack() },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: "fa-solid fa-turn-up" }),
                " Up one folder"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: "btn btn-sm btn-outline-primary", onClick: props.handleShowSearch },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: "fa-solid fa-magnifying-glass" }),
                " Show search")),
        transfer && (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "alert alert-success alert-dismissible col-8 fade show" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h4", { className: "alert-heading" }, "Accepted!"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", null, transfer["message"]),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("hr", null),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: "mb-0" },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("a", { className: "alert-link", href: `https://app.globus.org/activity/${transfer["task_id"]}`, target: "_blank" },
                    "Check Status of Request",
                    " ",
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: "fa-solid fa-arrow-up-right-from-square" }))),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { type: "button", className: "btn-close", "data-bs-dismiss": "alert", "aria-label": "Close" }))),
        apiError && (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "alert alert-danger alert-dismissible col-8 fade show" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("strong", null,
                "Error ",
                apiError.response.status,
                ": ",
                apiError.response.statusText,
                "."),
            " ",
            apiError.details && apiError.details,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { type: "button", className: "btn-close", "data-bs-dismiss": "alert", "aria-label": "Close" }))),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { id: "endpoint-list", className: "border col-8 rounded py-3" }, endpointList["DATA"].map((listItem, index) => {
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "form-check ms-3", key: index }, listItem["type"] == "dir" ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { className: "form-check-input", type: "checkbox", value: JSON.stringify(listItem), ref: (el) => (itemsRef.current[index] = el), onChange: handleEndpointSelect, "data-list-item-name": listItem["name"] }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.Link, { to: `/endpoints/${endpointID}/items/${listItem["name"]}?full-path=${endpointList["path"]}${listItem["name"]}` },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: "fa-solid fa-folder-open" }),
                        " ",
                        listItem["name"])))) : (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { className: "form-check-input", type: "checkbox", value: JSON.stringify(listItem), ref: (el) => (itemsRef.current[index] = el), onChange: handleEndpointSelect, "data-list-item-name": listItem["name"] }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: "fa-solid fa-file" }),
                    " ",
                    listItem["name"])))));
        })),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { id: "transfer-direction" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "btn-group mt-4" },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { type: "button", className: "btn btn-sm btn-outline-secondary", onClick: handleTransferToJupyter },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: "fa-solid fa-arrow-left" }),
                    " Transfer To JupyterLab"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { type: "button", className: "btn btn-sm btn-outline-secondary", onClick: handleTransferFromJupyter },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: "fa-solid fa-arrow-right" }),
                    " Transfer From JupyterLab"))))) : (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: "btn btn-sm btn-primary mb-2 mt-3", onClick: () => history.goBack() }, "Back"),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", null, "No files or folders found")))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Endpoint);


/***/ }),

/***/ "./lib/components/EndpointSearch.js":
/*!******************************************!*\
  !*** ./lib/components/EndpointSearch.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _Endpoint__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./Endpoint */ "./lib/components/Endpoint.js");
/* harmony import */ var _Endpoints__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./Endpoints */ "./lib/components/Endpoints.js");





const EndpointSearch = (props) => {
    const [apiError, setAPIError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [endpoints, setEndpoints] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({ DATA: [] });
    const [endpointValue, setEndpointValue] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const endpointSearch = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)();
    const history = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_1__.useHistory)();
    const handleEndpointClick = (event) => {
        // @ts-ignore
        endpointSearch.current.style.display = 'none';
    };
    const handleEndpointValueChange = (event) => {
        setEndpointValue(event.target.value);
    };
    const handleSearchEndpoints = async (event) => {
        let keyCode = event.keyCode;
        if (keyCode == 13) {
            setAPIError(null);
            setEndpoints({ DATA: [] });
            setLoading(true);
            try {
                let endpoints = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)(`endpoint_search?filter_fulltext=${endpointValue}`);
                setEndpoints(endpoints);
                setLoading(false);
                history.push('/endpoints');
            }
            catch (error) {
                setLoading(false);
                setAPIError(error);
            }
        }
    };
    const handleShowSearch = () => {
        // @ts-ignore
        endpointSearch.current.style.display = 'block';
    };
    if (apiError) {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { id: 'api-row', className: 'row' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'col-8' },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'alert alert-danger' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("strong", null,
                        "Error ",
                        apiError.response.status,
                        ": ",
                        apiError.response.statusText,
                        "."),
                    ' ',
                    "Please try again."))));
    }
    if (loading) {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h5", null, "Loading");
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { id: 'endpoint-search', className: 'mb-4' },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { ref: endpointSearch },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h5", null, "Search for Globus Collections"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'row' },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'col-8' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { id: 'endpoint-input', className: 'form-control', placeholder: 'Start typing and press enter to search', type: 'text', value: endpointValue, onChange: handleEndpointValueChange, onKeyDown: handleSearchEndpoints })))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_1__.Route, { exact: true, path: '/endpoints', render: (props) => {
                return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_Endpoints__WEBPACK_IMPORTED_MODULE_3__["default"], Object.assign({}, props, { endpoints: endpoints, handleEndpointClick: handleEndpointClick }));
            } }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_1__.Route, { exact: true, path: '/endpoints/:endpointID' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_Endpoint__WEBPACK_IMPORTED_MODULE_4__["default"], Object.assign({}, props, { selectedJupyterItems: props.selectedJupyterItems, handleShowSearch: handleShowSearch }))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_1__.Route, { path: '/endpoints/:endpointID/items/:path' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_Endpoint__WEBPACK_IMPORTED_MODULE_4__["default"], Object.assign({}, props, { selectedJupyterItems: props.selectedJupyterItems, handleShowSearch: handleShowSearch })))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (EndpointSearch);


/***/ }),

/***/ "./lib/components/Endpoints.js":
/*!*************************************!*\
  !*** ./lib/components/Endpoints.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


const Endpoints = (props) => {
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'row' }, props.endpoints['DATA'].length > 0 && (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'col-8' },
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'list-group' }, props.endpoints['DATA'].map((endpoint) => {
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.Link, { key: endpoint.id, to: `/endpoints/${endpoint.id}`, className: 'list-group-item list-group-item-action flex-column align-items-start', onClick: props.handleEndpointClick },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h5", { className: 'mb-1' },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: 'fa-solid fa-layer-group' }),
                    "\u00A0",
                    endpoint.display_name),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-0 mt-2 fw-bold' }, "Owner:"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-1' }, endpoint.owner_string),
                endpoint.description && (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-0 mt-2 fw-bold' }, "Description:"),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-1' }, endpoint.description)))));
        }))))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Endpoints);


/***/ }),

/***/ "./lib/components/GlobusObjects.js":
/*!*****************************************!*\
  !*** ./lib/components/GlobusObjects.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConfigAtom": () => (/* binding */ ConfigAtom),
/* harmony export */   "TransferAtom": () => (/* binding */ TransferAtom),
/* harmony export */   "TransferSelector": () => (/* binding */ TransferSelector)
/* harmony export */ });
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! recoil */ "webpack/sharing/consume/default/recoil/recoil");
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(recoil__WEBPACK_IMPORTED_MODULE_0__);

const ConfigAtom = (0,recoil__WEBPACK_IMPORTED_MODULE_0__.atom)({
    key: 'ConfigAtom',
    default: {
        collection_id: '',
        collection_base_path: '',
        is_gcp: false,
        is_hub: false,
        is_manual_copy_code_required: false,
        is_logged_in: false,
        collection_id_owner: '',
        last_login: null,
    },
});
const TransferAtom = (0,recoil__WEBPACK_IMPORTED_MODULE_0__.atom)({
    key: 'TransferAtom',
    default: {
        source_endpoint: '',
        destination_endpoint: '',
        transfer_items: [{
                source_path: '',
                destination_path: '',
                recursive: false
            }],
    },
});
const TransferSelector = (0,recoil__WEBPACK_IMPORTED_MODULE_0__.selector)({
    key: 'TransferSelector',
    get: ({ get }) => {
        return get(TransferAtom);
    },
    set: ({ get, set }, newTransferObject) => {
        let oldTransferObject = get(TransferAtom);
        let updatedTransferObject = Object.assign(Object.assign({}, oldTransferObject), newTransferObject);
        set(TransferAtom, updatedTransferObject);
    },
});


/***/ }),

/***/ "./lib/components/HubLoginWidget.js":
/*!******************************************!*\
  !*** ./lib/components/HubLoginWidget.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HubLogin": () => (/* binding */ HubLogin),
/* harmony export */   "HubLoginWidget": () => (/* binding */ HubLoginWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");



const HubLogin = (props) => {
    const [apiError, setAPIError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [hubInputCode, setHubInputCode] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const errorDetails = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const hubLoginButton = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        hubLoginButton.current.disabled = true;
    }, []);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if ("details" in props.hubResponse) {
            const errorDetailsDOM = errorDetails.current;
            const cleanErrorDetails = props.hubResponse.details.replace(/(?:\r\n|\\r\\n|\r|\n)/g, "<br/>");
            errorDetailsDOM.innerHTML = cleanErrorDetails;
        }
    }, [props]);
    const handleErrorDetails = (event) => {
        var text;
        if (errorDetails.current.classList.contains("hide-element")) {
            errorDetails.current.classList.remove("hide-element");
            errorDetails.current.classList.add("show-element");
            text = document.createTextNode("Hide Details");
        }
        else {
            errorDetails.current.classList.remove("show-element");
            errorDetails.current.classList.add("hide-element");
            text = document.createTextNode("Show Details");
        }
        event.target.removeChild(event.target.childNodes[0]);
        event.target.appendChild(text);
    };
    const handleHubInputChange = (event) => {
        if (event.target.value) {
            hubLoginButton.current.disabled = false;
        }
        setHubInputCode(event.target.value);
    };
    const handleHubLogin = async (event) => {
        event.preventDefault();
        try {
            await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)(`oauth_callback_manual?code=${hubInputCode}`);
        }
        catch (error) {
            setAPIError(error);
        }
    };
    if (apiError) {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "alert alert-danger alert-dismissible col-8 fade show" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("strong", null,
                "Error ",
                apiError.response.status,
                ": ",
                apiError.response.statusText,
                "."),
            " ",
            apiError.details && apiError.details,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", className: "btn-close", "data-bs-dismiss": "alert", "aria-label": "Close" })));
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "container mt-3" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "row" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "col-10" },
                apiError && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { id: "api-error", className: "alert alert-danger" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("strong", null,
                        "Error ",
                        apiError.response.status,
                        ": ",
                        apiError.response.statusText,
                        "."),
                    " ",
                    "Please try again.")),
                props.endpoint ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "mb-3 lead" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("i", { className: "fa-solid fa-circle-info" }),
                    " You must authenticate with the identity that is allowed to access this endpoint or collection.")) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "mb-3 lead" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("i", { className: "fa-solid fa-circle-info" }),
                    " Please log in and consent to JupyterLab performing a Globus transfer on your behalf.")),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ol", { className: "list-group" },
                    props.endpoint && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: "list-group-item p-4" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h5", { className: "mb-1" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("i", { className: "fa-solid fa-layer-group" }),
                            "\u00A0",
                            props.endpoint.display_name),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "mb-0 mt-2 fw-bold" }, "Owner:"),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "mb-1" }, props.endpoint.owner_string),
                        props.endpoint.description && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "mb-0 mt-2 fw-bold" }, "Description:"),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "mb-1" }, props.endpoint.description))))),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: "list-group-item p-4" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "ms-2 me-auto" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "fw-bold mb-3" },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "lead" }, "1. Log In to Globus to obtain an Authorization Code for this transfer")),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", className: "btn btn-outline-primary", onClick: () => {
                                    let loginURL = "login_url" in props.hubResponse
                                        ? props.hubResponse.login_url
                                        : (0,_handler__WEBPACK_IMPORTED_MODULE_2__.normalizeURL)("globus-jupyterlab/login");
                                    window
                                        .open(loginURL, "Globus Login", "height=600,width=800")
                                        .focus();
                                } }, "Log In to Globus"))),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: "list-group-item p-4" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "ms-2 me-auto" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "fw-bold mb-3" },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "lead" }, "2. Copy and paste the Authorization Code you just received from Globus")),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", { htmlFor: "code-input", className: "form-label" }, "Authorization Code"),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", id: "code-input", className: "form-control mb-3", name: "code-input", onChange: handleHubInputChange }),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", className: "btn btn-primary", ref: hubLoginButton, onClick: handleHubLogin }, "Continue"))),
                    "details" in props.hubResponse && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { className: "list-group-item" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "ms-2 me-auto my-3" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "btn btn-outline-primary", onClick: handleErrorDetails }, "Show details"),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "hide-element mt-3", ref: errorDetails })))))))));
};
class HubLoginWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(HubLogin, { endpoint: null, hubResponse: {} });
    }
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "normalizeURL": () => (/* binding */ normalizeURL),
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


function normalizeURL(endPoint = "") {
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, endPoint);
    return requestUrl;
}
/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = "", init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, "globus-jupyterlab", endPoint);
    let response;
    try {
        console.log("making request to: " + requestUrl);
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response);
    }
    return await response.json();
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "globus": () => (/* binding */ globus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _utilities__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./utilities */ "./lib/utilities.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _components_HubLoginWidget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/HubLoginWidget */ "./lib/components/HubLoginWidget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");








const addJupyterCommands = (app, commands) => {
    for (let command of commands) {
        app.commands.addCommand(command.command, {
            label: command.label,
            caption: command.caption,
            icon: _utilities__WEBPACK_IMPORTED_MODULE_4__.GlobusIcon,
            execute: command.execute,
        });
    }
};
/**
 * Globus plugin
 */
const globus = {
    id: "@jupyterlab/globus_jupyterlab",
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory],
    activate: activateGlobus,
};
async function activateGlobus(app, factory) {
    console.log("Globus Jupyterlab Extension Activated!");
    // GET request
    try {
        const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("config");
        console.log("Fetching basic data about the notebook server environment:", data);
        /*
          Commands to initiate a Globus Transfer.
          */
        let extensionCommands = [
            {
                command: "globus-jupyterlab-transfer/context-menu:open",
                label: "Initiate Globus Transfer",
                caption: "Login with Globus to Initiate Transfers",
                execute: async () => {
                    var files = factory.tracker.currentWidget.selectedItems();
                    var jupyterToken = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getToken();
                    var label = "Globus Jupyterlab Transfer";
                    let jupyterItems = [], fileCheck = true;
                    while (fileCheck) {
                        let file = files.next();
                        if (file) {
                            jupyterItems.push(file);
                        }
                        else {
                            fileCheck = false;
                        }
                    }
                    // Start creating the widget, but don't attach unless authenticated
                    const config = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("config");
                    const content = new _widget__WEBPACK_IMPORTED_MODULE_6__.GlobusWidget(config, factory, jupyterToken, jupyterItems);
                    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                    widget.title.label = label;
                    widget.title.icon = _utilities__WEBPACK_IMPORTED_MODULE_4__.GlobusIcon;
                    if (config.is_logged_in) {
                        app.shell.add(widget, "main");
                    }
                    else {
                        if (config.is_hub) {
                            const hubContent = new _components_HubLoginWidget__WEBPACK_IMPORTED_MODULE_7__.HubLoginWidget();
                            const hubWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({
                                content: hubContent,
                            });
                            hubWidget.title.label = "Authorization Code";
                            hubWidget.title.icon = _utilities__WEBPACK_IMPORTED_MODULE_4__.GlobusIcon;
                            app.shell.add(hubWidget, "main");
                        }
                        else {
                            window
                                .open((0,_handler__WEBPACK_IMPORTED_MODULE_5__.normalizeURL)("globus-jupyterlab/login"), "Globus Login", "height=600,width=800")
                                .focus();
                        }
                        // Poll for successful authentication.
                        let authInterval = window.setInterval(async () => {
                            const config = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)("config");
                            if (config.is_logged_in) {
                                app.shell.add(widget, "main");
                                clearInterval(authInterval);
                            }
                        }, 1000);
                    }
                },
            },
        ];
        addJupyterCommands(app, extensionCommands);
    }
    catch (error) {
        console.error(`Error activating Globus plugin.\n${error}`);
    }
}
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (globus);


/***/ }),

/***/ "./lib/utilities.js":
/*!**************************!*\
  !*** ./lib/utilities.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GlobusIcon": () => (/* binding */ GlobusIcon),
/* harmony export */   "getBaseURL": () => (/* binding */ getBaseURL)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);



const getBaseURL = (subPath = '') => {
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, subPath);
    return requestUrl;
};
const GlobusIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'globusIcon',
    svgstr: `
      <svg xmlns="http://www.w3.org/2000/svg" version="1.0" width="200.000000pt" height="200.000000pt" viewBox="0 0 200.000000 200.000000" preserveAspectRatio="xMidYMid meet">
        <g transform="translate(0.000000,200.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none">
          <path d="M480 1697 c-151 -51 -255 -148 -321 -297 -21 -49 -24 -69 -24 -180 0 -114 3 -131 28 -189 15 -36 24 -68 20 -71 -5 -4 -31 -23 -60 -44 -74 -52 -108 -123 -101 -209 12 -147 127 -268 315 -334 72 -26 90 -28 248 -29 94 0 188 -6 210 -12 146 -40 464 -41 659 -2 259 51 411 132 478 256 55 101 46 177 -30 252 -44 44 -46 49 -48 107 -2 106 -72 213 -167 256 -46 20 -167 26 -211 10 -23 -9 -27 -6 -54 43 -56 99 -149 158 -284 181 -32 5 -43 14 -71 58 -62 96 -156 167 -274 206 -88 29 -224 29 -313 -2z m307 -238 c15 -5 40 -22 56 -37 l27 -26 0 32 0 32 85 0 c69 0 85 -3 85 -15 0 -9 -9 -15 -22 -15 -12 0 -30 -7 -40 -17 -17 -15 -18 -37 -18 -272 0 -141 -4 -271 -9 -289 -5 -17 -6 -32 -2 -32 13 0 104 101 130 143 13 21 34 68 46 105 21 61 25 67 56 74 40 9 104 1 140 -18 30 -15 89 -79 89 -97 0 -7 4 -18 9 -26 7 -11 15 -10 42 10 50 36 151 39 199 7 53 -36 80 -83 80 -138 0 -40 4 -49 31 -69 74 -55 88 -132 39 -218 -79 -137 -270 -220 -535 -230 -150 -6 -282 11 -415 53 -73 23 -100 26 -193 24 -164 -3 -282 34 -352 111 -64 71 -54 141 26 181 41 22 83 23 158 4 50 -13 110 -20 151 -17 8 1 -9 12 -38 26 -41 19 -56 33 -68 60 -8 20 -12 40 -9 45 4 6 26 10 50 10 39 0 46 -4 60 -29 21 -41 53 -61 98 -61 47 0 89 21 104 52 7 12 15 58 18 101 7 77 0 93 -25 63 -6 -8 -32 -23 -56 -32 -64 -24 -141 -7 -193 45 -88 88 -96 292 -16 398 47 61 141 89 212 62z"/>
          <path d="M687 1400 c-41 -32 -62 -102 -62 -205 0 -110 21 -160 79 -189 33 -16 41 -17 74 -5 29 11 43 25 62 64 21 43 25 63 24 145 0 78 -4 104 -22 141 -33 69 -102 90 -155 49z"/>
        </g>
      </svg>
    `
});


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GlobusWidget": () => (/* binding */ GlobusWidget)
/* harmony export */ });
/* harmony import */ var _utilities__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./utilities */ "./lib/utilities.js");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! recoil */ "webpack/sharing/consume/default/recoil/recoil");
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(recoil__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _components_EndpointSearch__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./components/EndpointSearch */ "./lib/components/EndpointSearch.js");
/* harmony import */ var _components_GlobusObjects__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/GlobusObjects */ "./lib/components/GlobusObjects.js");
/* harmony import */ var _fortawesome_fontawesome_free_css_all_min_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @fortawesome/fontawesome-free/css/all.min.css */ "./node_modules/@fortawesome/fontawesome-free/css/all.min.css");
/* harmony import */ var bootstrap_dist_css_bootstrap_min_css__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");
/* harmony import */ var bootstrap_js_dist_alert_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! bootstrap/js/dist/alert.js */ "./node_modules/bootstrap/js/dist/alert.js");
/* harmony import */ var bootstrap_js_dist_alert_js__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_alert_js__WEBPACK_IMPORTED_MODULE_6__);










// Import specific bootstrap javascript plugins

const App = (props) => {
    // Local state values
    const [selectedJupyterItems, setSelectedJupyterItems] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)({ isEmpty: true });
    // Global Recoil state values
    const setConfig = (0,recoil__WEBPACK_IMPORTED_MODULE_3__.useSetRecoilState)(_components_GlobusObjects__WEBPACK_IMPORTED_MODULE_7__.ConfigAtom);
    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)(() => {
        setConfig(props.config);
    }, [props.config]);
    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)(() => {
        getJupyterItems();
    }, [props.jupyterItems]);
    const getJupyterItems = async () => {
        let directories = [];
        let files = [];
        let selectedJupyterItemsTemp = {};
        for (let file of props.jupyterItems) {
            try {
                let response = await fetch((0,_utilities__WEBPACK_IMPORTED_MODULE_8__.getBaseURL)(`api/contents/${file.path}`), {
                    headers: {
                        Accept: 'application/json',
                        Authorization: `token ${props.jupyterToken}`,
                        'Content-Type': 'application/json',
                    },
                });
                let temp = await response.json();
                if (temp.type == 'directory') {
                    directories.push(temp);
                }
                else {
                    files.push(temp);
                }
            }
            catch (error) {
                console.log(error);
            }
        }
        selectedJupyterItemsTemp['directories'] = directories;
        selectedJupyterItemsTemp['files'] = files;
        // If we have any file or folder, the payload is not empty
        if (directories.length || files.length) {
            selectedJupyterItemsTemp['isEmpty'] = false;
        }
        // Transfer direction inferred from selected files/folders
        if ((files.length && directories.length) || (files.length && !directories.length)) {
            selectedJupyterItemsTemp['transferDirection'] = 'toEndpoint';
        }
        else {
            selectedJupyterItemsTemp['transferDirection'] = 'toFromEndpoint';
        }
        //@ts-ignore
        setSelectedJupyterItems(selectedJupyterItemsTemp);
    };
    const handleLogout = async (event) => {
        event.preventDefault();
        await (0,_handler__WEBPACK_IMPORTED_MODULE_9__.requestAPI)('logout');
        window.open('https://globus.org/logout', 'Logout of Globus', 'height=600,width=800').focus();
        window.location.reload();
    };
    return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: 'container pt-5' },
        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: 'row' },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: 'col-8' },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("a", { href: '#', onClick: handleLogout },
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("i", { className: 'fa-solid fa-arrow-right-from-bracket' }),
                    " Logout of Globus"),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("hr", { className: 'mb-3 mt-3' }))),
        !selectedJupyterItems['isEmpty'] ? (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_components_EndpointSearch__WEBPACK_IMPORTED_MODULE_10__["default"], { factory: props.factory, selectedJupyterItems: selectedJupyterItems })) : (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { className: 'fw-bold text-danger' }, "No files selected"))));
};
class GlobusWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(config = {}, factory = null, jupyterToken = '', jupyterItems = []) {
        super();
        this.config = config;
        this.factory = factory;
        this.jupyterItems = jupyterItems;
        this.jupyterToken = jupyterToken;
        this.addClass('jp-ReactWidget');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.HashRouter, null,
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(recoil__WEBPACK_IMPORTED_MODULE_3__.RecoilRoot, null,
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.Switch, null,
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.Route, { path: '/', render: (props) => {
                            return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(App, Object.assign({}, props, { config: this.config, factory: this.factory, jupyterItems: this.jupyterItems, jupyterToken: this.jupyterToken })));
                        } })))));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.14fd355077c583bc042b.js.map