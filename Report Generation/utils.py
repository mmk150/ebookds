def date_scrape(month_input):
    month = month_input.partition("_")[0]
    day = int(month_input.partition("_")[2].partition("_")[0])
    match month:
        case "01":
            return "Jan",day
        case "02":
            return "Feb",day
        case "03":
            return "Mar",day
        case "04":
            return "Apr",day
        case "05":
            return "May",day
        case "06":
            return "Jun",day
        case "07":
            return "Jul",day
        case "08":
            return "Aug",day
        case "09":
            return "Sep",day
        case "10":
            return "Oct",day
        case "11":
            return "Nov",day
        case "12":
            return "Dec",day
        case _:
            print("error! ")
            return
