# Metric Definitions (Draft)

Definitions below favor junction-to-coolant conventions unless otherwise specified. Marked items are provisional pending confirmation from captured literature.

## Thermal resistance
- Standard: \(R_{th} = (T_{\text{hot}} - T_{\text{cold}}) / Q\) with temperatures referenced to consistent planes (e.g., junction-to-coolant inlet or wall-to-outlet). Units: K/W. Document the chosen reference planes per source.

## Pressure drop
- Standard: \(\Delta p = p_{\text{inlet}} - p_{\text{outlet}}\). Specify whether static or total pressure and the measurement locations.

## Pumping power
- Standard: \(P_{\text{pump}} = \Delta p \times \dot{V}\) where \(\dot{V}\) is volumetric flow rate. Note if corrected for pump efficiency; otherwise treat reported values as hydraulic power.

## Figure of merit
- Provisional: Use literature-reported FOMs when provided (e.g., \(1/(R_{th}\,\Delta p)\) or other normalized forms). When absent, annotate the intended form but keep it provisional until a consistent definition is selected.

## Flow uniformity
- Provisional: Quantify uniformity via standard deviation or coefficient of variation of branch/channel mass flow relative to the mean. Record how each source defines and measures it.

## Manufacturability proxy
- Provisional: Track reported minimum feature size, wall thickness, overhang limits, and any manufacturability score used by the source. Treat any aggregated index as provisional until cross-source agreement is found.

## Structural screening metrics
- Provisional: Record von Mises stress, displacement, or safety factor under coolant pressure and thermal loads when reported. Note boundary conditions and material properties; treat derived pass/fail thresholds as provisional unless the source cites standards.

