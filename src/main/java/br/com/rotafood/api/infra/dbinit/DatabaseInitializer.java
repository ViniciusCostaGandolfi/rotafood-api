package br.com.rotafood.api.infra.dbinit;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import br.com.rotafood.api.modules.catalog.application.service.DefaultPackagingPopulateService;
import br.com.rotafood.api.modules.catalog.application.service.DefaultProductPopulateService;

@Component
public class DatabaseInitializer implements CommandLineRunner {

    @Value("${database.init}")
    private boolean databaseInit;

    @Autowired
    private DefaultProductPopulateService defaultProductPopulateService;

    @Autowired
    private DefaultPackagingPopulateService defaultPackagingPopulateService;


    @Override
    public void run(String... args) throws Exception {
        if (databaseInit) {
            String jsonFilePathProduct = "src/main/resources/db/populate/populateDbDefaultProduct2.json";
            defaultProductPopulateService.populateDatabase(jsonFilePathProduct);
            System.out.println("Database default products populated successfully!");
    
            String jsonFilePathPackaging = "src/main/resources/db/populate/populateDbDefaultPackaging.json";
            defaultPackagingPopulateService.populateDatabase(jsonFilePathPackaging);
            System.out.println("Database default products populated successfully!");
        }
    }
}
