package br.com.rotafood.api.modules.common.application.service;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

import br.com.rotafood.api.infra.config.minio.MinioStorageService;
import br.com.rotafood.api.modules.merchant.domain.entity.Image;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.ImageRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;

@Service
public class ImageService {

    @Autowired
    private ImageRepository imageRepository;

    @Autowired
    private MinioStorageService minioStorageService;

    @Autowired
    private MerchantRepository merchantRepository;

    @Value("${minio.bucket.name}")
    private String bucketName;

    @Value("${minio.url}")
    private String minioUrl;

    @Transactional
    public Image uploadImage(MultipartFile file, UUID merchantId) {
        String contentType = file.getContentType();
        if (contentType == null || (!contentType.equals("image/png") && !contentType.equals("image/jpeg"))) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Apenas arquivos PNG ou JPEG são permitidos.");
        }

        try {
            UUID id = UUID.randomUUID();
            
            String fileExtension = contentType.equals("image/png") ? ".png" : ".jpeg";

            String fileName = "images/" + id.toString() + fileExtension;

            try (InputStream inputStream = file.getInputStream()) {
                minioStorageService.uploadFile(bucketName, fileName, inputStream, contentType);
            }

            Merchant merchant = this.merchantRepository.getReferenceById(merchantId);
            Image image = new Image();
            image.setPath(minioUrl + "/" + bucketName + "/" + fileName);
            image.setId(id);
            image.setMerchant(merchant);

            return imageRepository.save(image);

        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Erro ao processar o arquivo.", e);
        }
    }

    @Transactional
    public void deleteByIdAndMerchantId(UUID imageId, UUID merchantId) {
        Image image = imageRepository.findByIdAndMerchantId(imageId, merchantId);
    
        if (image == null) {
            throw new IllegalArgumentException("Imagem não encontrada ou não pertence ao Merchant especificado.");
        }
    
        String imagePath = image.getPath();
        if (imagePath == null) {
            throw new IllegalArgumentException("Caminho da imagem não encontrado.");
        }

        String fileKey = imagePath.replace(minioUrl + "/" + bucketName + "/", "");

        minioStorageService.deleteFile(bucketName, fileKey);

        imageRepository.delete(image);
    }
    
    public Image getByIdAndMerchantId(UUID imageId, UUID merchantId) {
        return imageRepository.findByIdAndMerchantId(imageId, merchantId);
    }

    public List<Image> getAllByMerchantId(UUID merchantId) {
        return imageRepository.findAllByMerchantId(merchantId);
    }
}
