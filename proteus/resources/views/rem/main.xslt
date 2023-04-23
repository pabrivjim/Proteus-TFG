<xsl:stylesheet
        version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:exslt="http://exslt.org/common"
        xmlns:msxsl="urn:schemas-microsoft-com:xslt"
        xmlns:proteus="https://proteus.us.es"
        exclude-result-prefixes="exslt msxsl">
    <xsl:output method="html" doctype-public="XSLT-compat" omit-xml-declaration="yes" encoding="UTF-8" indent="yes"/>

    <!-- Object templates -->
    <xsl:include href="objects/figure.xslt" />
    <xsl:include href="objects/requirements.xslt" />
    <xsl:include href="objects/paragraph.xslt" />
    <xsl:include href="objects/section.xslt" />
    <xsl:include href="objects/default.xslt" />

    <xsl:template match="/">
        <html>
            <head>
                <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" integrity="sha512-wnea99uKIC3TJF7v4eKk4Y+lMz2Mklv18+r4na2Gn1abDRPPOeef95xTzdwGD9e6zXJBteMIhZ1+68QC5byJZw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            </head>
            <body class="body h-full">
                <div class="mx-auto max-w-[210mm] w-full md:w-1/2 p-10 print:m-0 print:w-full">
                    <xsl:apply-templates />    
                </div>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="document">
          <img
            src="https://www.informatica.us.es/docs/imagen-etsii/logo-ETSII-Color.png"
            class="h-12 my-5"
        />
        
        <!-- Title -->
        <h1 class="text-2xl roboto">
            <xsl:value-of select="properties/string" />
        </h1>
        
        <!-- Document properties -->
        <dl class="py-3 dl">
            <xsl:for-each    select="properties/*">
                <dt class="font-bold capitalize"><xsl:value-of select="proteus:trans(string(@name))"/>:</dt>
                    <dd class=""><xsl:value-of select="."/></dd>
            </xsl:for-each>
        </dl>

        <!-- Table of contents -->
        <h2 class="title text-2xl dl my-2 font-bold">
            <xsl:value-of name="pStringTableOfContents" select="proteus:trans('Table of contents')" disable-output-escaping="yes"/>
        </h2>
        <ol>
            <xsl:for-each select="children/object"> 
                <li class="ml-3 text-lg underline text-blue-600">
                    <a href="#{@id}" style="font-weight:bold; visited:text-blue-600">
                        <xsl:call-template name="table_of_contents"/>
                    </a>
                    <xsl:if test="children/object">
                        <ol>
                            <xsl:for-each select="children/object"> 
                                <li class="ml-5 underline text-blue-600">
                                    <a href="#{@id}">
                                        <xsl:call-template name="table_of_contents"/>
                                    </a>
                                </li>
                            </xsl:for-each>
                        </ol>
                    </xsl:if>
                </li>
            </xsl:for-each>
        </ol>
        <hr class="mt-3" />

        <!-- Document objects -->
        <xsl:for-each select="children/object">              
            <xsl:call-template name="child" />
        </xsl:for-each>

    </xsl:template>

    <xsl:template name="table_of_contents">
        <xsl:choose>
            <xsl:when test="properties/*[@name='identifier']">
                <xsl:value-of select="concat(properties/*[@name='name'], ': ', properties/*[@name='identifier'])" disable-output-escaping="yes"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="properties/*[@name='name']" disable-output-escaping="yes"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="child">
        <xsl:call-template name="object"/>
        <xsl:for-each select="children/object">
            <div class="ml-2">
                <xsl:call-template name="child"/>
            </div>
        </xsl:for-each>
    </xsl:template>

    
    <xsl:template name="object">
        <!-- List of the classes that should use the requirements template -->
        <xsl:variable name="requirements">|actor|useCase|objective|informationRequirement|functionalRequirement|constraintRequirement|nonFunctionalRequirement|</xsl:variable>
        <xsl:variable name="class" select="@classes"/>
        <xsl:choose>
            <xsl:when test="$class = 'section'">
                <xsl:call-template name="section"/>
            </xsl:when>
            <xsl:when test="$class = 'paragraph'">
                <xsl:call-template name="paragraph"/>
            </xsl:when>
            <xsl:when test="contains($requirements,$class)">
                <xsl:call-template name="requirements"/>
            </xsl:when>
            <xsl:when test="$class = 'figure'">
                <xsl:call-template name="figure"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="default"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

<xsl:template name="proteus_table">
    <xsl:param name="version"/>
    <xsl:param name="description"/>
    <xsl:param name="comments"/>
    <xsl:param name="preCondition"/>
    <xsl:param name="postCondition"/>
    <xsl:param name="stability"/>
    <xsl:param name="developmentState"/>
    <xsl:param name="urgency"/>
    <tr>
      <th class="capitalize align-top">
        <xsl:value-of name="pStringVersion" select="concat(proteus:trans('Version'), ':')" disable-output-escaping="yes"/>
      </th>
      <td class="pl-5">
        <ul>
          <li><xsl:value-of select="$version"/></li>
        </ul>
      </td>
    </tr>
    <tr>
      <th class="capitalize align-top">
        <xsl:value-of name="pStringDescription" select="concat(proteus:trans('Description'), ':')" disable-output-escaping="yes"/>
      </th>
      <td class="pl-5">
        <ul>
          <li><xsl:value-of select="$description"/></li>
        </ul>
      </td>
    </tr>
    <xsl:if test="not(@classes = 'actor')">
        <xsl:if test="not($stability = 'PD')">
        <tr>
            <th class="capitalize align-top">
                <xsl:value-of name="pStringStability" select="concat(proteus:trans('stability'), ':')" disable-output-escaping="yes"/>
            </th>
            <td class="pl-5">
                <ul>
                <li><xsl:value-of select="$stability"/></li>
                </ul>
            </td>
        </tr>
        </xsl:if>
        <xsl:if test="not($developmentState = 'PD')">
        <tr>
            <th class="capitalize align-top">
                <xsl:value-of name="pStringDevelopmentState" select="concat(proteus:trans('developmentState'), ':')" disable-output-escaping="yes"/>
            </th>
            <td class="pl-5">
                <ul>
                <li><xsl:value-of select="$developmentState"/></li>
                </ul>
            </td>
        </tr>  
        </xsl:if>
        <xsl:if test="not($urgency = 'PD')">
        <tr>
            <th class="capitalize align-top">
                <xsl:value-of name="pStringUrgency" select="concat(proteus:trans('urgency'), ':')" disable-output-escaping="yes"/>
            </th>
            <td class="pl-5">
                <ul>
                <li><xsl:value-of select="$urgency"/></li>
                </ul>
            </td>
        </tr>  
        </xsl:if>
    </xsl:if>
    <!-- If the object is a use case, the preCondition and postCondition are shown. -->
    <xsl:if test="@classes = 'useCase'">
        <tr>
            <th class="capitalize align-top">
                <xsl:value-of name="pStringPrecondition" select="concat(proteus:trans('preCondition'), ':')" disable-output-escaping="yes"/>
            </th>
            <td class="pl-5">
                <ul>
                <li><xsl:value-of select="$preCondition"/></li>
                </ul>
            </td>
        </tr>
        <tr>
            <th class="capitalize align-top">
                <xsl:value-of name="pStringPostcondition" select="concat(proteus:trans('postCondition'), ':')" disable-output-escaping="yes"/>
            </th>
            <td class="pl-5">
                <ul>
                <li><xsl:value-of select="$postCondition"/></li>
                </ul>
            </td>
        </tr>  
    </xsl:if>
    <tr>
      <th class="
      capitalize align-top">
        <xsl:value-of name="pStringComments" select="concat(proteus:trans('Comments'), ':')" disable-output-escaping="yes"/>
      </th>
      <td class="pl-5">
        <ul>
          <li><xsl:value-of select="$comments"/></li>
        </ul>
      </td>
    </tr>
  </xsl:template>


</xsl:stylesheet>