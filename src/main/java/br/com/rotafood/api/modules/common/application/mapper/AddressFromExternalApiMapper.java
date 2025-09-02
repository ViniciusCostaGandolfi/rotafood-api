package br.com.rotafood.api.modules.common.application.mapper;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.order.application.dto.BrasilApiResponse;
import com.google.maps.model.AddressComponentType;
import com.google.maps.model.GeocodingResult;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.Arrays;

@Component
public class AddressFromExternalApiMapper {
    
    public AddressDto fromBrasilApiResponse(BrasilApiResponse response) {
        if (response == null) return null;
        
        String formattedAddress = String.format("%s, %s, %s - %s",
                response.street(), response.neighborhood(), response.city(), response.state());

        return new AddressDto(
            null,
            "Brasil",
            response.state(),
            response.city(),
            response.neighborhood(),
            response.cep(),
            response.street(),
            "S/N",
            formattedAddress,
            "",
            response.location() != null ? response.location().latitude() : BigDecimal.ZERO,
            response.location() != null ? response.location().longitude() : BigDecimal.ZERO
        );
    }

    public AddressDto fromGeocodingResult(GeocodingResult result) {
        if (result == null) return null;
        
        return new AddressDto(
            null,
            extractComponent(result, AddressComponentType.COUNTRY, false),
            extractComponent(result, AddressComponentType.ADMINISTRATIVE_AREA_LEVEL_1, false),
            extractComponent(result, AddressComponentType.ADMINISTRATIVE_AREA_LEVEL_2, false),
            getNeighborhoodFromResult(result),
            extractComponent(result, AddressComponentType.POSTAL_CODE, false),
            extractComponent(result, AddressComponentType.ROUTE, false),
            getStreetNumberFromResult(result),
            result.formattedAddress,
            "",
            BigDecimal.valueOf(result.geometry.location.lat),
            BigDecimal.valueOf(result.geometry.location.lng)
        );
    }

    public boolean isResultComplete(GeocodingResult result) {
        if (result == null) {
            return false;
        }
        boolean hasStreet = !extractComponent(result, AddressComponentType.ROUTE, false).isBlank();
        boolean hasPostalCode = !extractComponent(result, AddressComponentType.POSTAL_CODE, false).isBlank();
        boolean hasNeighborhood = !getNeighborhoodFromResult(result).isBlank();
        boolean hasCity = !extractComponent(result, AddressComponentType.ADMINISTRATIVE_AREA_LEVEL_2, false).isBlank();
        boolean hasState = !extractComponent(result, AddressComponentType.ADMINISTRATIVE_AREA_LEVEL_1, false).isBlank();
        boolean hasCountry = !extractComponent(result, AddressComponentType.COUNTRY, false).isBlank();

        return hasStreet && hasPostalCode && hasNeighborhood && hasCity && hasState && hasCountry;
    }

    private String getNeighborhoodFromResult(GeocodingResult result) {
        String neighborhood = extractComponent(result, AddressComponentType.SUBLOCALITY_LEVEL_1, false);
        if (neighborhood == null || neighborhood.isBlank()) {
            return extractComponent(result, AddressComponentType.NEIGHBORHOOD, false);
        }
        return neighborhood;
    }

    private String getStreetNumberFromResult(GeocodingResult result) {
        String streetNumber = extractComponent(result, AddressComponentType.STREET_NUMBER, false);
        return (streetNumber == null || streetNumber.isBlank()) ? "S/N" : streetNumber;
    }

    private String extractComponent(GeocodingResult result, AddressComponentType type, boolean useShortName) {
        if (result == null || result.addressComponents == null) return "";
        return Arrays.stream(result.addressComponents)
                .filter(c -> c.types != null && Arrays.asList(c.types).contains(type))
                .findFirst()
                .map(c -> useShortName ? c.shortName : c.longName)
                .orElse("");
    }
}