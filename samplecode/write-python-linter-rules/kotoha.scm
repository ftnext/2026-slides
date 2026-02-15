(typed_parameter
  (identifier) @param_name
  type: (type
    (generic_type
      (identifier) @type_name
      (type_parameter
        (type
          (identifier) @inner_type))))
  (#eq? @type_name "list"))
