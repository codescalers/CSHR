<script lang="ts">
  import type { CertificateType } from '../../types';
  export let certificates: CertificateType[];
</script>

<div class="col-md-6">
  <div class="card mb-4 mb-md-0">
    <div class="card-body">
      <p class="mb-4">
        <span class="text-primary font-italic me-1"
          ><i class="bi bi-bookmark-fill icon" /></span
        >
        Certificates
      </p>
      {#each certificates as certificate, index (index)}
        <div class="d-flex flex-row justify-content-between">
          <p class="my-2 name">
            {certificate.name}
          </p>
          <a
            class="btn btn-primary my-0"
            href={certificate.certificate_link + ''}
            rel="noopener noreferrer"
            target="_blank"
          >
            check certificate
          </a>
        </div>
      {/each}
    </div>
  </div>
</div>
