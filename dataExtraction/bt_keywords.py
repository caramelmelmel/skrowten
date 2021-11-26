# File location keywords
BT_RESULTS_DIR = "browsertime-results"
BT_JSON = "browsertime.json"
BT_HAR = "browsertime.har"
CSV_FILE = "cleaned_data" # cleaned_data_STARTTIME.csv
EXTRACT_DATA_DIR = "extract_data"
PLOT_DIR = "plot_dir"
BT_CUSTOM_DIR = "BrowserTimeResults"
CUSTOM_HTTP2_DIR = "HTTP2_testing"
CUSTOM_HTTP3_DIR = "HTTP3_testing"

HTTP_DIR_LIST = [CUSTOM_HTTP2_DIR, CUSTOM_HTTP3_DIR]

NUM_HTTP2_REPONSES = "num_http2_responses"
NUM_HTTP3_REPONSES = "num_http3_responses"

# SpeedIO also uses browsertime
SPEED_IO_ROOT_DIR = "sitespeed-result"
# results are in pages/PAGE_NAME/data
SPEED_IO_PAGE_DIR = "pages"
SPEED_IO_DATA_DIR = "data"
SPEED_IO_HAR = "browsertime.har"
SPEED_IO_JSON = "browsertime.pageSummary.json"
SPEED_IO_LIGHTHOUSE = "lighthouse.pageSummary.json"

# JSON keywords
BROWSERSCRIPTS = "browserScripts"

# Har Keywords
HAR_ROOT = "log"
HAR_ENTRIES = "entries"
HAR_HTTP_RESPONSE = 'response'
# log.entries.response.httpVersion
HAR_HTTP_VERSION_SUB = "httpVersion"
BT_HTTP_VERSION_3 = "HTTP/3"

# sitespeed io http3
SITESPEED_HTTP_VERSION_3 = "h3"


# Keywords used in the browsertime.json file
# There might be a better way to organise this. 
class BTJsonArgs:
    # Root json keys
    FAILURE = "markedAsFailure" 
    STATISTICS = "statistics"
    INFO = "info"

    # Json Keys that lead to more sub jsons
    STAT_PAGE_INFO = "pageinfo"
    STAT_TIMINGS = "timings"
    NAV_TIMING = "navigationTiming"

    STAT_COACH = "coach"
    STAT_COACH_ADVICE = "coachAdvice"
    STAT_COACH_ADVICE_ADVICE = "advice"
    STAT_COACH_ADVICE_ADVICE_INFO = "info"

    # Interested Sub Jsons 
    TTFB = "ttfb"
    LOADED_EVENT_END = "loadEventEnd" 
    FIRST_PAINT = "firstPaint"
    FULLY_LOADED = "fullyLoaded"

    DOM_COMPLETE = "domComplete"
    DOM_ELEMENTS = "domElements"

    CONNECTIVITY = "connectivity"
    PROFILE = "profile"
    TIMESTAMP = "timestamp" 
    URL = "url" 

    # stats wanted
    MEDIAN = "median"
    MEAN = "mean"
    MIN = "min"
    MAX ="max"

    # info.connectivity
    INFO_LIST = [
        TIMESTAMP, URL
    ]

    # statistics.coach.coachAdvice.advice.info
    STATS_COACH_ADVICE_INFO_LIST = [
        DOM_ELEMENTS,
    ]

    # statistics.timings
    STATS_TIMING_LIST = [
        TTFB,
        LOADED_EVENT_END , 
        FIRST_PAINT, 
        FULLY_LOADED
    ]

    # statistics.timings.navigationTiming
    STATS_NAV_TIMING_LIST = [
        DOM_COMPLETE, 
    ]    

    # states wanted from each statistics page
    STATS_WANTED = [
        MEDIAN,
        MEAN,
        MIN,
        MAX,
    ]

class LighthouseJsonArgs:
    # performance keywords
    CATEGORIES = "categories"    
    PERFORMANCE = "performance"
    PERFORMANCE_TITLE = "lighthouse_performance"

    # audit keywords
    AUDITS = "audits"
    SCORE = "score"
    NUMERIC_VALUE = "numericValue"
    
    # Audit titles
    FIRST_CONTENTFUL_PAINT = "first-contentful-paint"
    LARGEST_CONTENTFUL_PAINT = "largest-contentful-paint"
    SPEED_INDEX = "speed-index"
    TOTAL_BLOCKING_TIME = "total-blocking-time"
    CUMULATIVE_LAYOUT_SHIFT = "cumulative-layout-shift"

    # stats wanted
    MEDIAN = "median"
    MEAN = "mean"

    # CATEGORIES.PERFORMANCE
    GET_SCORE_LIST = [
        CATEGORIES, PERFORMANCE
    ]

    PERFORMANCE_STAT_KEYS = [
        MEDIAN,
        MEAN,
    ]

    ADUITS_LIST = [
        FIRST_CONTENTFUL_PAINT, 
        LARGEST_CONTENTFUL_PAINT, 
        SPEED_INDEX, 
        TOTAL_BLOCKING_TIME, 
        CUMULATIVE_LAYOUT_SHIFT
    ]