# 将尝试用python实现
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

_uwsgi_common() {
    env UWSGI_VASSAL_VIRTUALENV="$PY_ENV" \
        UWSGI_VASSAL_SET="base_dir=$BASE" uwsgi \
        --virtualenv="$PY_ENV" \
        --pidfile="$ENV_RUN_PATH/avalon.pid" \
        --log-maxsize="$UWSGI_LOG_MAXSIZE" \
        --cpu-affinity="$UWSGI_CPU_AFFINITY" \
        --emperor="$UWSGI_EMPEROR" \
        $@ \
        --memory-report \
        --log-zero \
        --log-slow \
        --log-4xx \
        --log-5xx \
        --log-big \
        --log-sendfile
}

uwsgi_start() {
    echo -n "Starting $UWSGI_DESC: "
    if kill -0 $(cat $UWSGI_PIDFILE 2>/dev/null) 2>/dev/null; then
        echo_error "failed."
        echo "  $UWSGI_NAME is already running."
    else
        _uwsgi_common --daemonize="$UWSGI_LOGFILE"
        echo_info "$UWSGI_NAME."
    fi
}

uwsgi_debug() {
    echo -n "Starting $UWSGI_DESC: "
    if kill -0 $(cat $UWSGI_PIDFILE 2>/dev/null) 2>/dev/null; then
        echo_error "failed."
        echo "  $UWSGI_NAME is already running."
    else
        _uwsgi_common --catch-exceptions
        echo_info "$UWSGI_NAME."
    fi
}

uwsgi_reload() {
    echo -n "Reloading $UWSGI_DESC: "
    source "$PY_ENV/bin/activate"
    error=$(uwsgi --reload $UWSGI_PIDFILE 2>&1 >/dev/null)
    if [ -z "$error" ]; then
        echo_info "$UWSGI_NAME."
    else
        echo_error "failed."
        echo "  $error"
    fi
}

uwsgi_stop() {
    echo -n "Stopping $UWSGI_DESC: "
    source "$PY_ENV/bin/activate"
    error=$(uwsgi --stop $UWSGI_PIDFILE 2>&1 >/dev/null)
    if [ -z "$error" ]; then
        echo_info "$UWSGI_NAME."
    else
        echo_error "failed."
        echo "  $error"
    fi
}

uwsgi_restart() {
    uwsgi_stop
    while kill -0 $(cat $UWSGI_PIDFILE 2>/dev/null) 2>/dev/null ; do
        echo -n '.'
    done
    uwsgi_start
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

        local vassal="$PY_ENV/etc/uwsgi/vassals/$app.json"
        if [ ! -f $vassal ]; then
            echo_info "Adding App $app..."
            python $BASE/tools/uwsgi_conf.py $conf > $vassal
        fi
    done
}

_manage_list() {
    local APPS=$@

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
        local vassal="$PY_ENV/etc/uwsgi/vassals/$app.json"
        if [ -e $vassal ]; then
            echo_info "Removing app $app..."
        fi
        rm -f "$vassal"
    done
}

_manage_log() {
    local LOG_PATH=$BASE/.py/var/log/avalon.log
    tail -f $LOG_PATH
}

manage() {
    local ACTION=$1
    local APPS=${@:2}
    UWSGI_LOG_MAXSIZE=268435456
    UWSGI_CPU_AFFINITY=2
    UWSGI_EMPEROR="$PY_ENV/etc/uwsgi/vassals"
    UWSGI_PIDFILE="$ENV_RUN_PATH/avalon.pid"
    UWSGI_DESC="Avalon"
    UWSGI_NAME="avalon"
    UWSGI_LOGFILE="$PY_ENV/var/log/avalon.log"

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
        # TODO
        update)
            _manage_update $APPS
            ;;
        # TODO
        touch)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_reload
            fi
            _manage_touch $APPS
            ;;
        # TODO
        test)
            _manage_test $2
            RC=$?
            ;;
        # TODO
        test_no_return)
            manage test --no-return
            ;;
        # TODO
        start)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_restart
            fi
            uwsgi_start
            ;;
        # TODO
        debug)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_restart
            fi
            uwsgi_debug
            ;;
        # TODO
        console)
            _manage_console $2
            ;;
        # TODO
        shell)
            _manage_shell $2
            ;;
        # TODO
        stop)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_stop
            fi
            uwsgi_stop
            ;;
        # TODO
        restart|force-reload)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_restart
            fi
            uwsgi_restart
            ;;
        # TODO
        reload)
            if [ "$GUOKR_ENVIRON" != "PRODUCTION" ]; then
                nginx_reload
            fi
            uwsgi_reload
            ;;
        # TODO
        clear)
            _manage_clear $APPS
            ;;
        # TODO
        create_dbs)
            _manage_create_dbs
            ;;
        # TODO
        create_tables)
            _manage_create_tables
            ;;
        # TODO
        create_app)
            _manage_create_app $APPS
            ;;
        # TODO
        cronsync)
            _manage_cronsync $APPS
            ;;
        # TODO
        cronlist)
            _manage_cronlist $APPS
            ;;
        # TODO
        jar)
            _manage_jar
            ;;
        # TODO
        uberjar)
            _manage_uberjar
            ;;
        # TODO
        log)
            _manage_log
            ;;
        # TODO
        jenkins)
            $BASE/tools/jenkins/jenkinshelper.py ${@:2}
            ;;
        # TODO
        review)
            _manage_review $2
            ;;
        # TODO
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
        # TODO
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
        # TODO
            echo "Usage: manage { add | remove | list | start | test | debug | stop | console | shell | clear | reload | touch | restart | force-reload | create_dbs | create_tables | create_app | cronsync | cronlist | jar | uberjar | celery }"
            ;;
    esac

    return $RC
}

complete_manage(){
    echo
}

complete -F complete_manage manage
