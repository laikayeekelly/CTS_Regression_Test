<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <TestPlan version="1.0">
        <xsl:for-each select="TestResult/TestPackage">
            <xsl:if  test="count(TestSuite//TestCase/Test[@result='fail' or  @result='timeout' ]) &gt; 0" >
                <xsl:variable name="package"><xsl:value-of select="@appPackageName"/></xsl:variable>
                <Entry uri="{$package}"/>
            </xsl:if>
        </xsl:for-each>
        </TestPlan>
    </xsl:template>
</xsl:stylesheet>
 