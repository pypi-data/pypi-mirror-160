message(STATUS "Build Documentation")
find_package(Doxygen
                 REQUIRED dot
                 OPTIONAL_COMPONENTS mscgen dia)
if (DOXYGEN_FOUND)
        include(GNUInstallDirs)
        find_program(DOXYGEN_EXECUTABLE doxygen REQUIRED)
        set(DOXYGEN_PROJECT_NAME "${PROJECT_NAME}")
        set(DOXYGEN_PROJECT_BRIEF "${PROJECT_DESCRIPTION}")
        
        
        set(DOXYGEN_RECURSIVE YES)
        set(DOXYGEN_GENERATE_HTML YES)
        
#        set(DOXYGEN_CREATE_SUBDIRS YES)

        set(DOXYGEN_ALLOW_UNICODE_NAMES YES) 
        set(DOXYGEN_OUTPUT_LANGUAGE "Japanese-en")
        set(DOXYGEN_DOXYFILE_ENCODING "UTF-8")
        
#        set(DOXYGEN_OUTPUT_TEXT_DIRECTION "ltr")

        set(DOXYGEN_BRIEF_MEMBER_DESC YES)
        set(DOXYGEN_REPEAT_BRIEF YES)
        #set(DOXYGEN_INLINE_INHERITED_MEMB YES)
        set(DOXYGEN_INHERIT_DOCS YES)
        set(DOXYGEN_DISTRIBUTE_GROUP_DOC YES)
        set(DOXYGEN_GROUP_NESTED_COMPOUNDS YES)
        #set(DOXYGEN_INLINE_GROUPED_CLASSES YES)
        #set(DOXYGEN_INLINE_SIMPLE_STRUCTS YES)
        
#        set(DOXYGEN_HTML_DYNAMIC_MENUS YES)
        
        set(DOXYGEN_CHM_INDEX_ENCODING "UTF-8")

#        set(DOXYGEN_HTML_DYNAMIC_SECTIONS YES)
        set(DOXYGEN_HTML_TIMESTAMP YES)
        set(DOXYGEN_ALWAYS_DETAILED_SEC YES)
        set(DOXYGEN_JAVADOC_AUTOBRIEF YES)
        set(DOXYGEN_FULL_PATH_NAMES NO)
        set(DOXYGEN_SHORT_NAMES NO)
        set(DOXYGEN_MULTILINE_CPP_IS_BRIEF NO)
        set(DOXYGEN_INHERIT_DOCS YES)
        
#        set(DOXYGEN_SEPARATE_MEMBER_PAGES YES)
        set(DOXYGEN_TAB_SIZE 4)
        
        set(DOXYGEN_MARKDOWN_SUPPORT YES)
        set(DOXYGEN_AUTOLINK_SUPPORT YES)
        set(DOXYGEN_BUILTIN_STL_SUPPORT NO)
        set(DOXYGEN_CPP_CLI_SUPPORT YES)
        set(DOXYGEN_IDL_PROPERTY_SUPPORT YES)
        set(DOXYGEN_SUBGROUPING YES)
        set(DOXYGEN_EXTRACT_ALL YES)
        set(DOXYGEN_EXTRACT_PRIVATE YES)
        set(DOXYGEN_EXTRACT_PACKAGE YES)
        set(DOXYGEN_EXTRACT_PRIV_VIRTUAL YES)
        set(DOXYGEN_EXTRACT_STATIC YES)
        set(DOXYGEN_EXTRACT_LOCAL_CLASSES YES)
        set(DOXYGEN_EXTRACT_LOCAL_METHODS YES)
        set(DOXYGEN_EXTRACT_ANON_NSPACES YES)
        set(DOXYGEN_SHOW_GROUPED_MEMB_INC YES)
        
#        set(DOXYGEN_FORCE_LOCAL_INCLUDES YES)

        set(DOXYGEN_INLINE_INFO YES)
        set(DOXYGEN_SORT_MEMBER_DOCS YES)
        set(DOXYGEN_SHOW_USED_FILES YES)
        set(DOXYGEN_SHOW_FILES YES)
        set(DOXYGEN_SHOW_NAMESPACES YES)
        set(DOXYGEN_INPUT_ENCODING "UTF-8")
        set(DOXYGEN_REFERENCES_LINK_SOURCE YES) 
        set(DOXYGEN_SOURCE_TOOLTIPS YES)
#        set(DOXYGEN_ALPHABETICAL_INDEX YES)
        set(DOXYGEN_GENERATE_TREEVIEW YES)
        set(DOXYGEN_USE_MATHJAX YES)
        
#        set(DOXYGEN_MACRO_EXPANSION YES)
#        set(DOXYGEN_EXPAND_ONLY_PREDEF YES)
#        set(DOXYGEN_PREDEFINED "extern=//")
#        set(DOXYGEN_EXPAND_AS_DEFINED "extern")
        
        set(DOXYGEN_CALL_GRAPH YES)
        set(DOXYGEN_CALLER_GRAPH YES)
        set(DOXYGEN_DOT_GRAPH_MAX_NODES 10000)
        set(DOXYGEN_MAX_DOT_GRAPH_DEPTH 1000)
        set(DOXYGEN_DIR_GRAPH_MAX_DEPTH 25)
        set(DOXYGEN_HAVE_DOT YES)
        set(DOXYGEN_DOT_MULTI_TARGETS YES)
        set(DOXYGEN_CLASS_DIAGRAMS YES)
        set(DOXYGEN_CLASS_GRAPH YES)
        set(DOXYGEN_COLLABORATION_GRAPH YES)
        set(DOXYGEN_DIRECTORY_GRAPH YES)
        set(DOXYGEN_INCLUDE_GRAPH YES)
        set(DOXYGEN_INCLUDED_BY_GRAPH YES)
#        set(DOXYGEN_DOT_CLEANUP YES)
        
        #set(DOXYGEN_DOT_TRANSPARENT YES)
        set(DOXYGEN_DOT_UML_DETAILS YES)
        set(DOXYGEN_GRAPHICAL_HIERARCHY YES)
        set(DOXYGEN_GROUP_GRAPHS YES)
        set(DOXYGEN_INCLUDE_GRAPH YES)
        set(DOXYGEN_INCLUDED_BY_GRAPH YES)
        #set(DOXYGEN_INTERACTIVE_SVG YES)
        set(DOXYGEN_REFERENCED_BY_RELATION YES)
        set(DOXYGEN_REFERENCES_RELATION YES)
        
        #set(DOXYGEN_UML_LIMIT_NUM_FIELDS 100)
        
        set(DOXYGEN_USE_MDFILE_AS_MAINPAGE "${PROJECT_SOURCE_DIR}/README.md")
        
        doxygen_add_docs(cxxjij_header_only_docs
                         ${PROJECT_SOURCE_DIR}/src ${PROJECT_SOURCE_DIR}/openjij ${PROJECT_SOURCE_DIR}/README.md
                         ALL
                         COMMENT "Generate documentation with Doxygen")
        install(DIRECTORY ${PROJECT_BINARY_DIR}/html
                DESTINATION ${PROJECT_SOURCE_DIR}/docs) 
else() 
        message(SEND_ERROR "building documentation (-DBUILD_DOCS=ON) is enabled, but doxygen not found")
endif()
