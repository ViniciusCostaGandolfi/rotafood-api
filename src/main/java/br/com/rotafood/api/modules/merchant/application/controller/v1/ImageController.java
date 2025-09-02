package br.com.rotafood.api.modules.merchant.application.controller.v1;

import br.com.rotafood.api.modules.catalog.application.dto.ImageDto;
import br.com.rotafood.api.modules.common.application.service.ImageService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import java.util.List;
import java.util.UUID;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;

@RestController
@RequestMapping( ApiVersion.VERSION + "/merchants/{merchantId}/images")
public class ImageController {

    @Autowired
    private ImageService imageService;

    
    @GetMapping
    public List<ImageDto> getAllImages(@PathVariable UUID merchantId) {
        return imageService.getAllByMerchantId(merchantId)
                .stream()
                .map(ImageDto::new)
                .toList();
    }

    @GetMapping("/{imageId}")
    public ImageDto getImageById(@PathVariable UUID merchantId, @PathVariable UUID imageId) {
        return new ImageDto(imageService.getByIdAndMerchantId(imageId, merchantId));
    }

    @PutMapping
    public ImageDto uploadImage(
            @PathVariable UUID merchantId,
            @RequestParam("image") MultipartFile imageFile) {
        return new ImageDto(imageService.uploadImage(imageFile, merchantId));
    }

    @DeleteMapping("/{imageId}")
    public void deleteImage(@PathVariable UUID merchantId, @PathVariable UUID imageId) {
        imageService.deleteByIdAndMerchantId(imageId, merchantId);
    }
}
