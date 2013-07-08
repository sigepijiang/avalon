echo_info() {
    echo -e "\033[0;32;1m$1\033[0m"
}

echo_warning() {
    echo -e "\033[0;33;1m$1\033[0m"
}

echo_error() {
    echo -e "\033[0;31;1m$1\033[0m"
}

get_all_confs() {                                                        
    if [ -d "$BASE/avalon/apps" ]; then
        echo $(find $BASE/avalon/apps -name "app.yaml")                       
    fi
    if [ -d "$BASE/avalon/services" ]; then
        echo $(find $BASE/avalon/services -name "app.yaml")                       
    fi
    if [ -d "$BASE/avalon/algo" ]; then
        echo $(find $BASE/avalon/algo -name "app.yaml")                       
    fi
}                                                                        
                                                                         
get_all_apps() {                                                         
    for conf in $(get_all_confs); do                                     
        echo $(dirname $conf|xargs basename)                             
    done                                                                 
}

get_conf() {
    for vassal in $(get_all_confs); do
        v=$(echo $vassal|grep $1/app.yaml)
        if [ -n "$v" ]; then
            echo $v
            return
        fi
    done
}

goodbye() {
    deactivate
    unset BASE
    unset PY_ENV
    unset PYLIB_PATH
    unset TOOL_PATH
    unset UWSGI_CONFIG_PATH
    unset NGINX_CONFIG_PATH
    unset ENV_RUN_PATH
    unset ENV_LOG_PATH
    unset AVALON_ENVIRON
}

_manage_add() {
    local APPS=$@

    if [ -z "$APPS" ]; then
       APPS=$(get_all_apps)
    fi

    for app in $APPS; do
        local conf=$(get_conf $app)
        if [ -z "$conf" ]; then
            echo_error "App $app not found."
            return 1
        fi

        local vassal="${UWSGI_CONFIG_PATH}/${app}.json"
        if [ ! -f $vassal ]; then
            echo_info "Adding App $app..."
            python $BASE/tools/uwsgi_conf.py $conf > $vassal
        fi
    done
}

_manage_list() {
    APPS=$@

    if [ -z "$APPS" ]; then
        APPS=$(get_all_apps)
    fi

    for app in $APPS; do
        echo_info "${app}"
    done
}

_manage_remove() {
    local APPS=$@
    if [ -z "$APPS" ]; then
        APPS=$(get_all_apps)
    fi

    for app in $APPS; do
        local vassal="${UWSGI_CONFIG_PATH}/${app}.json"
        if [ -e $vassal ]; then
            echo_info "Removing app $app..."
        fi
        rm -f "$vassal"
    done
}

manage() {
    local ACTION=$1
    local APPS=${@:2}
    local UWSGI_LOG_MAXSIZE=268435456

    case $1 in
        add)
            _manage_add $APPS
            ;;
        remove)
            _manage_remove $APPS
            ;;
        list)
            _manage_list $APPS
            ;;
        update)
            _manage_update $APPS
            ;;
        touch)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_reload
            fi
            _manage_touch $APPS
            ;;
        test)
            _manage_test $2
            RC=$?
            ;;
        test_no_return)
            manage test --no-return
            ;;
        start)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_restart
            fi
            uwsgi_start
            ;;
        debug)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_restart
            fi
            uwsgi_debug
            ;;
        console)
            _manage_console $2
            ;;
        shell)
            _manage_shell $2
            ;;
        stop)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_stop
            fi
            uwsgi_stop
            ;;
        restart|force-reload)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_restart
            fi
            uwsgi_restart
            ;;
        reload)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_reload
            fi
            uwsgi_reload
            ;;
        clear)
            _manage_clear $APPS
            ;;
        create_dbs)
            _manage_create_dbs
            ;;
        create_tables)
            _manage_create_tables
            ;;
        create_app)
            _manage_create_app $APPS
            ;;
        cronsync)
            _manage_cronsync $APPS
            ;;
        cronlist)
            _manage_cronlist $APPS
            ;;
        jar)
            _manage_jar
            ;;
        uberjar)
            _manage_uberjar
            ;;
        log)
            _manage_log
            ;;
        jenkins)
            $BASE/tools/jenkins/jenkinshelper.py ${@:2}
            ;;
        review)
            _manage_review $2
            ;;
        celery)
            case $2 in
                restart)
                    celery_restart
                    ;;
                *)
                    echo "Usage: manage celery { restart }"
                    ;;
            esac
            ;;
        nginx)
            case $2 in
                start)
                    nginx_start
                    ;;
                stop)
                    nginx_stop
                    ;;
                restart)
                    nginx_restart
                    ;;
                reload)
                    nginx_reload
                    ;;
                test)
                    nginx_test
                    ;;
                render)
                    nginx_render
                    ;;
                *)
                    echo "Usage: manage nginx { start | stop | restart | reload | test | render }"
                    ;;
            esac
            ;;
        *)
            echo "Usage: manage { add | remove | list | start | test | debug | stop | console | shell | clear | reload | touch | restart | force-reload | create_dbs | create_tables | create_app | cronsync | cronlist | jar | uberjar | celery }"
            ;;
    esac

    return $RC
}

complete_manage(){
    echo
}

complete -F complete_manage manage
