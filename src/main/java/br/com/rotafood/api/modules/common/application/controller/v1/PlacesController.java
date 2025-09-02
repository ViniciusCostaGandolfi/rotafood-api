package br.com.rotafood.api.modules.common.application.controller.v1;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.common.application.service.PlacesService;

@RestController
@RequestMapping(ApiVersion.VERSION + "/places")
@Validated
public class PlacesController {

    private final PlacesService placesService;

    public PlacesController(PlacesService placesService) {
        this.placesService = placesService;
    }

    @GetMapping("/cep/{cep}")
    public AddressDto getAddressByCep(
        @PathVariable
        @Pattern(regexp = "\\d{8,9}", message = "CEP deve conter 8 ou 9 dígitos numéricos")
        String cep
    ) {
        return placesService.findByCep(cep);
    }


    @GetMapping("/search")
    public List<AddressDto> searchByAddress(
        @RequestParam @Size(min = 5, message = "Digite pelo menos 5 caracteres") String q
    ) {
        return placesService.searchByAddress(q);
    }

    @GetMapping("/reverse-geocoding")
    public AddressDto getAddressByCoordinates(
        @RequestParam @NotNull BigDecimal latitude,
        @RequestParam @NotNull BigDecimal longitude
    ) {
        return placesService.reverseGeocode(latitude, longitude);
    }
}
