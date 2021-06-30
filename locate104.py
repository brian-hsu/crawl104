class LocateOneZeroFour:

    @property
    def css_locate(self):
        css_selector = dict()
        css_selector["search_keyword"] = dict()
        css_selector["search_keyword"].update({"keyword": "#keyword"})
        css_selector["search_keyword"].update({"submit-buttons": ".whole-submit-button"})
        css_selector["search_keyword"].update({"search-type": "#searchType"})

        css_selector["job_cate"] = dict()
        css_selector["job_cate"].update({"job_cate": "#jobCateLauncher"})
        # css_selector["job_cate"].update({"result-item": ".item-data"})
        css_selector["job_cate"].update({"result-list": "form.cate-menu .result-list"})
        css_selector["job_cate"].update({"submit": ".menu-content .filter-submit"})

        css_selector["exclusion_condition"] = dict()
        css_selector["exclusion_condition"].update({"title_button": "form > .tertiary-button > .collapse-arrow"})
        css_selector["exclusion_condition"].update({"styled-select": ".tertiary > li > .styled-select"})
        css_selector["exclusion_condition"].update({"exclude_select": "li > .styled-select > #searchTempExclude"})

        css_selector["whole_submit"] = dict()
        css_selector["whole_submit"].update({"whole_submit": "form > .buttons > #searchSubmit"})
        css_selector["whole_submit"].update({"job-list": "#joblist .job-list"})
        css_selector["whole_submit"].update({"next_page": ".pages-box > .pnext"})

        css_selector["search_area"] = dict()
        css_selector["search_area"].update({"whole_submit": "form > .buttons > #searchSubmit"})
        css_selector["search_area"].update({"area_menu": "#area-menu > .scene > .frt-cate"})
        css_selector["search_area"].update({"area_tw": '#area-menu .frt-cate > li[data-no="6001000000"]'})
        css_selector["search_area"].update({"tw_label": '#area-menu .scd-cate:nth-child(2) .scd-class > label'})
        css_selector["search_area"].update({"area_button": '#area-menu > .buttons > .yellow'})



        return css_selector
