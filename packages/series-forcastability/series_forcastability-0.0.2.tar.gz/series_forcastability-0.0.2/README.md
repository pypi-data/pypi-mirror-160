# Determine series forecastability

### Instructions

1. Install:

        pip install series_forcastability


2. Determine series forecastability based on the series characteristics

        from series_forcastability import main
        # Check series forecastability
        cov = main.sf(series).forecastability()
