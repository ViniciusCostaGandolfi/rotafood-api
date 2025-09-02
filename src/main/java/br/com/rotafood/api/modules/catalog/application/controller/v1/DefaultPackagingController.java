package br.com.rotafood.api.modules.catalog.application.controller.v1;

import br.com.rotafood.api.modules.catalog.application.dto.DefaultPackagingDto;
import br.com.rotafood.api.modules.merchant.domain.repository.DefaultPackagingRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping( ApiVersion.VERSION + "/default-packagings")
public class DefaultPackagingController {

    @Autowired
    private DefaultPackagingRepository defaultPackagingRepository;

    @GetMapping
    public List<DefaultPackagingDto> getAllDefaultPackaging(@RequestParam(required = false) String search) {
        if (search == null || search.isBlank()) {
            return defaultPackagingRepository.findAll(PageRequest.of(0, 30))
                    .stream()
                    .map(DefaultPackagingDto::new)
                    .toList();
        }

        return defaultPackagingRepository.findByNameContaining(
                search,
                PageRequest.of(0, 30)
        ).stream().map(DefaultPackagingDto::new).toList();
    }

}
