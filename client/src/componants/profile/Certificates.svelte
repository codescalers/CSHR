<script lang="ts">
    import type { CertificateType } from '../../utils/types';
    export let certificates: CertificateType[];
  </script>
  
<div class="col-md-6">
    <div class="card mb-4 mb-md-0">
        <div class="card-header">
            Certificates
        </div>
        <div class="card-body">
            {#each certificates as certificate, index (index)}
                <div class="d-flex flex-row justify-content-between">
                    <p class="my-2 name">
                        {certificate.name}
                    </p>
                    <a
                        class="btn text-primary my-0"
                        href={certificate.certificate_link}
                        rel="noopener noreferrer"
                        target="_blank"
                    >
                        check certificate
                    </a>
                </div>
            {:else}
                ---
            {/each}
        </div>
    </div>
</div>
  